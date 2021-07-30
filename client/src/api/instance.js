/*
 * @Description:
 * @Version: 1.0
 * @Autor: Tu Ruwei
 * @Date: 2021-07-08 16:07:31
 * @LastEditors: Tu Ruwei
 * @LastEditTime: 2021-07-09 12:37:08
 */
import request from '@/utils/cors-request'

export function post_instance_status_control(name, params) {
  return request({
    url: '/api/instance_status_control/' + name,
    method: 'post',
    params
  })
}
export function post_instance_resize_cmd(name, params) {
  return request({
    url: '/api/instance_resize_cmd/' + name,
    method: 'post',
    params
  })
}
export function get_instance_resize_cmd(name) {
  return request({
    url: '/api/instance_resize_cmd/' + name,
    method: 'get'
  })
}

export function get_instances_info() {
  return request({
    url: '/api/instances_info',
    method: 'get'
  })
}

export function get_instance_info(name) {
  return request({
    url: '/api/instance_info/' + name,
    method: 'get'
  })
}

export function get_instance_image_info(name) {
  return request({
    url: '/api/instance_image_info/' + name,
    method: 'get'
  })
}

export function upload_instance_image(name, params) {
  return request({
    url: '/api/upload_instance_image/' + name,
    method: 'post',
    data: params
  })
}

export function upload_instance_image_info() {
  return request({
    url: '/api/upload_instance_image_info',
    method: 'get'
  })
}
