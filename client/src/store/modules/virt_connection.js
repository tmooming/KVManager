// import { get_connect_info } from '@/api/connection'
import { setVirt_connect_token, getVirt_connect_token } from '@/utils/virt-info'
// import { resetRouter } from '@/router'

const getDefaultState = () => {
  return {
    host: '',
    name: '',
    passwd: '',
    type: '',
    virt_connect_token: getVirt_connect_token() ? getVirt_connect_token() : ''
  }
}

const state = getDefaultState()

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_HOST: (state, host) => {
    state.host = host
  },
  UPDATE_HOST: (state, host) => {
    state.host = host
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_PASSWD: (state, passwd) => {
    state.passwd = passwd
  },
  SET_TYPE: (state, type) => {
    state.type = type
  },
  SET_VIRT_CONNECT_TOKEN: (state, virt_connect_token) => {
    state.virt_connect_token = virt_connect_token
  }
}

const actions = {
  // virt connection
  connection({ commit }, connect_info) {
    const { host, name, passwd, type } = connect_info.info
    return new Promise((resolve, reject) => {
      commit('virt_connection/SET_HOST', host, { root: true })
      commit('virt_connection/SET_NAME', name, { root: true })
      commit('virt_connection/SET_PASSWD', passwd, { root: true })
      commit('virt_connection/SET_TYPE', type, { root: true })
      commit('virt_connection/SET_VIRT_CONNECT_TOKEN', connect_info.token, { root: true })
      setVirt_connect_token(connect_info.token)
      resolve().catch(error => {
        reject(error)
      })
    })
  },

  // get connect info
  get_host_info({ commit, state }, data) {
    return new Promise((resolve, reject) => {
      // commit('virt_connection/UPDATE_HOST', data.host, { root: true })
      // commit('virt_connection/SET_NAME', data.name, { root: true })
      // commit('virt_connection/SET_PASSWD', data.passwd, { root: true })
      // commit('virt_connection/SET_TYPE', data.type, { root: true })
      // commit('virt_connection/SET_VIRT_CONNECT_TOKEN', data.virt_connect_tokens, { root: true })
      // setVirt_connect_token(data.virt_connect_tokens)
      resolve().catch(error => {
        reject(error)
      })
    })
  },

  // // user logout
  // logout({ commit, state }) {
  //   return new Promise((resolve, reject) => {
  //     logout(state.token).then(() => {
  //       removeToken() // must remove  token  first
  //       resetRouter()
  //       commit('RESET_STATE')
  //       resolve()
  //     }).catch(error => {
  //       reject(error)
  //     })
  //   })
  // },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      // removeToken() // must remove  token  first
      commit('RESET_STATE')
      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

