/*
 * @Description:
 * @Version: 1.0
 * @Autor: Tu Ruwei
 * @Date: 2021-07-08 16:07:31
 * @LastEditors: Tu Ruwei
 * @LastEditTime: 2021-07-09 16:15:57
 */
import request from '@/utils/cors-request'

export function connect_openstack(params) {
  return request({
    url: '/api/openstack_connect',
    method: 'post',
    data: params
  })
}
export function disconnect_openstack(params) {
  return request({
    url: '/api/openstack_disconnect',
    method: 'get',
    params
  })
}

export function get_openstack_info() {
  return request({
    url: '/api/openstack_connect',
    method: 'get'
  })
}

export function get_openstack_image_lists(id_md5) {
  return request({
    url: '/api/image_lists/' + id_md5,
    method: 'get'
  })
}
export function update_image_args(id, params) {
  return request({
    url: '/api/image_update/' + id,
    method: 'patch',
    data: params
  })
}
export function upload_image(name, params) {
  return request({
    url: '/api/image_upload/' + name,
    method: 'put',
    data: params
  })
}
export function upload_image_info() {
  return request({
    url: '/api/image_upload_info',
    method: 'get'
  })
}
