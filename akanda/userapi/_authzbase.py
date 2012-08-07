import abc

from sqlalchemy.orm import exc as sa_exc

from quantum import quota
from quantum.api.v2 import attributes
from quantum.api.v2 import base
from quantum.api.v2 import resource as api_resource
from quantum.common import exceptions as q_exc
from quantum.openstack.common import cfg


class ResourcePlugin(object):
    """
    """
    JOINS = ()
    def __init__(self, delegate):
        # synthesize the hooks because Quantum's base class uses the
        # resource name as part of the method name
        setattr(self, 'get_%s' % delegate.collection_name, self._get_collection)
        setattr(self, 'get_%s' % delegate.resource_name, self._get_item)
        setattr(self, 'update_%s' % delegate.resource_name, self._update_item)
        setattr(self, 'create_%s' % delegate.resource_name, self._create_item)
        setattr(self, 'delete_%s' % delegate.resource_name, self._delete_item)
        self.delegate = delegate

    def _get_tenant_id_for_create(self, context, resource):
        if context.is_admin and 'tenant_id' in resource:
            tenant_id = resource['tenant_id']
        elif ('tenant_id' in resource and
              resource['tenant_id'] != context.tenant_id):
            reason = _('Cannot create resource for another tenant')
            raise q_exc.AdminRequired(reason=reason)
        else:
            tenant_id = context.tenant_id
        return tenant_id

    def _model_query(self, context):
        query = context.session.query(self.delegate.model)

        # NOTE(jkoelker) non-admin queries are scoped to their tenant_id
        if not context.is_admin and hasattr(self.delegate.model, 'tenant_id'):
            query = query.filter(
                self.delegate.model.tenant_id == context.tenant_id)

        return query

    def _get_collection(self, context, filters=None, fields=None,
                        verbose=None):
        collection = self._model_query(context)
        if filters:
            for key, value in filters.iteritems():
                column = getattr(self.delegate.model, key, None)
                if column:
                    collection = collection.filter(column.in_(value))
        return [self._fields(self.delegate.make_dict(c), fields) for c in
                collection.all()]

    def _get_by_id(self, context, id, verbose=None):
        try:
            query = self._model_query(context)
            if verbose:
                if verbose and isinstance(verbose, list):
                    options = [orm.joinedload(join) for join in
                               self.delegate.joins if join in verbose]
                else:
                    options = [orm.joinedload(join) for join in
                               self.delegate.joins]
                query = query.options(*options)
            return query.filter_by(id=id).one()
        except sa_exc.NoResultFound:
            raise q_exc.NotFound()

    def _get_item(self, context, id, fields=None, verbose=None):
        obj = self._get_by_id(context, id, verbose=verbose)
        return self._fields(self.delegate.make_dict(obj), fields)

    def _update_item(self, id, **kwargs):
        key = self.delegate.resource_name
        resource_dict = kwargs[key][key]
        obj = self._get_by_id(context, id, verbose=verbose)
        return self.delegate.update(obj, resource_dict)

    def _create_item(self, context, **kwargs):
        key = self.delegate.resource_name
        resource_dict = kwargs[key][key]
        tenant_id = self._get_tenant_id_for_create(context, resource_dict)
        return self.delegate.create(tenant_id, resource_dict)

    def _delete_item(self, context, id):
        obj = self._get_by_id(context, id, verbose=verbose)
        with context.session.begin():
            self.delegate.before_delete(obj)
            context.session.delete(obj)

    def _fields(self, resource, fields):
        if fields:
            return dict([(key, item) for key, item in resource.iteritems()
                        if key in fields])
        return resource


class ResourceDelegate(object):
    """
    """
    __metaclass__ = abc.ABCMeta

    def before_delete(self, resource):
        pass

    @abc.abstractproperty
    def model(self):
        pass

    @abc.abstractproperty
    def resource_name(self):
        pass

    @abc.abstractproperty
    def collection_name(self):
        pass

    @property
    def joins(self):
        return ()

    @abc.abstractmethod
    def update(self, tenant_id, resource, body):
        pass

    @abc.abstractmethod
    def create(self, tenant_id, body):
        pass

    @abc.abstractmethod
    def make_dict(self, obj):
        pass


def create_extension(delegate):
    """
    """
    #for key, value in delegate.ATTRIBUTE_MAP.iteritems():
    #    if key in attributes.RESOURCE_ATTRIBUTE_MAP:
    #        pass # TODO(mark): should log that we're doing this
    #    attributes.RESOURCE_ATTRIBUTE_MAP[key] = value
    return api_resource.Resource(base.Controller(ResourcePlugin(delegate),
                                                 delegate.collection_name,
                                                 delegate.resource_name,
                                                 delegate.ATTRIBUTE_MAP))


def register_quota(resource_name, config_key_name, default=-1):
    """
    """
    quota_opt = cfg.IntOpt(config_key_name,
                           default=default,
                           help=('number of %s allowed per tenant, -1 for '
                                 'unlimited' % resource_name))
    cfg.CONF.register_opts([quota_opt], 'QUOTAS')
    quota.QUOTAS.register_resource(
        quota.CountableResource(resource_name,
                                quota._count_resource,
                                config_key_name))