"""
    *************************** 
    --------description-------- 
 	 Description: 
 	 Version: 1.0
 	 Autor: Tu Ruwei
 	 Date: 2021-07-13 17:18:43
 	 LastEditors: Tu Ruwei
 	 LastEditTime: 2021-07-14 15:29:08

    ***************************  
"""
#!/usr/bin/env python
# -*- encoding: utf-8 -*-


from resources.kvm.connection import (
    HostInfo,
    HostDetail,
    HostStoragesInfo,
    HostNetsInfo,
    HostInterfacesInfo,
    HostNwfiltersInfo,
    HostSecretsInfo,
    HostDisconnect,
    HostHistoryInfo
)
from resources.kvm.instance import (
    InstancesInfo,
    InstanceInfo,
    InstanceDetail,
    InstanceStatusControl,
    InstanceResizeCMD,
    InstanceImageInfo,
    InstanceImageUpload,
    InstanceUploadPrepareInfo
)
from resources.openstack.connection import (
    OpenstackConnect,
    OpenstackDisconnect
)
from resources.openstack.image import (
    ImagesDetail,
    ImageUpdate,
    ImageUpload,
    ImageUploadInfo
)


def initialize_routes(api):
    # api.add_resource(UserList, '/api/users', endpoint='user_list_view')
    # api.add_resource(UserDetail, '/api/users/<id>', endpoint='user_detail_view')
    api.add_resource(HostInfo, '/api/host_info', endpoint='host_info')
    api.add_resource(HostDetail, '/api/host_detail', endpoint='host_detail')
    api.add_resource(HostStoragesInfo, '/api/host_storages_info', endpoint='host_storages_info')
    api.add_resource(HostNetsInfo, '/api/host_nets_info', endpoint='host_nets_info')
    api.add_resource(HostHistoryInfo, '/api/host_history_info',endpoint='host_history_info')
    api.add_resource(HostInterfacesInfo, '/api/host_interfaces_info', endpoint='host_interfaces_info')
    api.add_resource(HostNwfiltersInfo, '/api/host_nwfilters_info', endpoint='host_nwfilters_info')
    api.add_resource(HostSecretsInfo, '/api/host_secrets_info', endpoint='host_secrets_info')
    api.add_resource(HostDisconnect, '/api/host_disconnect/<hostname>', endpoint='host_disconnect')

    api.add_resource(InstancesInfo, '/api/instances_info', endpoint='instances_info')
    api.add_resource(InstanceInfo, '/api/instance_info/<name>', endpoint='instance_info')
    api.add_resource(InstanceDetail, '/api/instance_detail/<name>', endpoint='instance_detail')
    api.add_resource(InstanceStatusControl, '/api/instance_status_control/<name>', endpoint='instance_status_control')
    api.add_resource(InstanceResizeCMD, '/api/instance_resize_cmd/<name>', endpoint='instance_resize_cmd')
    api.add_resource(InstanceImageInfo, '/api/instance_image_info/<name>', endpoint='instance_image_info')
    api.add_resource(InstanceImageUpload, '/api/upload_instance_image/<name>', endpoint='upload_instance_image')
    api.add_resource(InstanceUploadPrepareInfo, '/api/upload_instance_image_info/<uuid>', endpoint='upload_instance_image_info')

    api.add_resource(OpenstackConnect, '/api/openstack_connect', endpoint='openstack_connect')
    api.add_resource(OpenstackDisconnect, '/api/openstack_disconnect', endpoint='openstack_disconnect')
    api.add_resource(ImagesDetail, '/api/image_lists/<id_md5>', endpoint='openstack_image_lists')
    api.add_resource(ImageUpdate, '/api/image_update/<id>', endpoint='glance_image_update')
    api.add_resource(ImageUpload, '/api/image_upload/<name>', endpoint='glance_image_upload')
    api.add_resource(ImageUploadInfo, '/api/image_upload_info/<uuid>', endpoint='glance_image_upload_info')
