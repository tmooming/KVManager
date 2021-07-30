/*
 * @Description:
 * @Version: 1.0
 * @Autor: Tu Ruwei
 * @Date: 2021-07-13 17:09:13
 * @LastEditors: Tu Ruwei
 * @LastEditTime: 2021-07-14 15:32:15
 */
import request from '@/utils/cors-request'

export function get_host_info() {
  return request({
    url: '/api/host_info',
    method: 'get'
  })
}

export function connect_host(params) {
  return request({
    url: '/api/host_info',
    method: 'post',
    params

  })
}
export function disconnect_host(hostname) {
  return request({
    url: '/api/host_disconnect/' + hostname,
    method: 'get'
  })
}
export function get_host_detail() {
  return request({
    url: '/api/host_detail',
    method: 'get'
  })
}

export function get_host_history_info() {
  return request({
    url: '/api/host_history_info',
    method: 'get'
  })
}
export function get_host_storages_info() {
  return request({
    url: '/api/host_storages_info',
    method: 'get'
  })
}

export function get_host_nets_info() {
  return request({
    url: '/api/host_nets_info',
    method: 'get'
  })
}

export function get_host_interfaces_info() {
  return request({
    url: '/api/host_interfaces_info',
    method: 'get'
  })
}

export function get_host_nwfilters_info() {
  return request({
    url: '/api/host_nwfilters_info',
    method: 'get'
  })
}

export function get_host_secrets_info() {
  return request({
    url: '/api/host_secrets_info',
    method: 'get'
  })
}
