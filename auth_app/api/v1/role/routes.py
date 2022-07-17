from . import role_api
from .role_create import RoleCreate
from .role_list import RoleList
from .role_remove import RoleRemove
from .role_retrieve import RoleRetrieve
from .role_update import RoleUpdate
from .role_user_remove import RoleUserRemove
from .role_user_set import RoleUserSet

role_api.add_resource(RoleList, "/")
role_api.add_resource(RoleUserSet, "/add")
role_api.add_resource(RoleCreate, "/create")
role_api.add_resource(RoleUpdate, "/update")
role_api.add_resource(RoleUserRemove, "/delete")
role_api.add_resource(RoleRetrieve, "/<string:role_id>")
role_api.add_resource(RoleRemove, "/delete/<string:role_id>")
