const getters = {
  sidebar: state => state.app.sidebar,
  device: state => state.app.device,
  user_token: state => state.user.token,
  user_avatar: state => state.user.avatar,
  user_name: state => state.user.name,
  virt_host: state => state.virt_connection.host,
  virt_name: state => state.virt_connection.name,
  virt_passwd: state => state.virt_connection.passwd,
  virt_type: state => state.virt_connection.type,
  virt_token: state => state.virt_connection.token

}
export default getters
