import Cookies from 'js-cookie'

const Instance_name = 'Instance_name'
const Virt_connect_token = 'Virt_connect_token'

export function getInstance_name() {
  return Cookies.get(Instance_name) ? Cookies.get(Instance_name) : 'none'
}
export function getVirt_connect_token() {
  return Cookies.get(Virt_connect_token) ? Cookies.get(Virt_connect_token) : 'none'
}
export function setInstance_name(instance_name) {
  return Cookies.set(Instance_name, instance_name)
}
export function setVirt_connect_token(virt_connect_token) {
  return Cookies.set(Virt_connect_token, virt_connect_token)
}
export function removeInstance_name() {
  return Cookies.remove(Instance_name)
}
export function removeVirt_connect_token() {
  return Cookies.remove(Virt_connect_token)
}
