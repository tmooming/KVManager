import axios from 'axios'
import { Message } from 'element-ui'
// import store from '@/store'
import { getVirt_connect_token } from '@/utils/virt-info'
// axios.defaults.withCredentials = true
// create an axios instance
const service = axios.create({
  baseURL: 'http://10.122.110.80:5000', // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 1000 * 60 * 60, // request timeout:60 mins
  withCredentials: true
})

// request interceptor
service.interceptors.request.use(
  config => {
    // do something before request is sent

    if (getVirt_connect_token() !== 'none') {
      // let each request carry token
      // ['X-Token'] is a custom headers key
      // please modify it according to the actual situation
      config.headers['Authorization'] = getVirt_connect_token()
    }
    return config
  },
  error => {
    // do something with request error
    console.log(error) // for debug
    return Promise.reject(error)
  }
)
// response interceptor
service.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
  */

  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  response => {
    const res = response.data
    const status = response.status
    // if the custom code is not 20000, it is judged as an error.
    if (status >= 400) {
      Message({
        message: res.message,
        type: 'warning',
        duration: 1000
      })
      // if (status === 404) {
      //   Message({
      //     message: res.message,
      //     type: 'warning',
      //     duration: 1000
      //   })
      // } else if (status === 400) {
      //   Message({
      //     message: res.message,
      //     type: 'warning',
      //     duration: 1000
      //   })
      // }
      // // 50008: Illegal token; 50012: Other clients logged in; 50014: Token expired;
      // if (res.code === 404 || res.code === 400 || res.code === 50014) {
      //   // to re-login
      //   MessageBox.confirm('错误', 'Confirm logout', {
      //     confirmButtonText: 'Re-Login',
      //     cancelButtonText: 'Cancel',
      //     type: 'warning'
      //   }).then(() => {
      //     store.dispatch('user/resetToken').then(() => {
      //       location.reload()
      //     })
      //   })
      // }
      return Promise.reject(new Error(res.message || 'Error'))
    } else {
      if (status === 204) {
        Message({
          message: res.message || '操作成功',
          type: 'success',
          duration: 5 * 1000
        })
      }
      return Promise.resolve(res)
    }
  },
  // },
  error => {
    // console.log('开始' + error.request.status + '结束') // for debug
    console.log('-------------------')
    console.log(error.request)
    if (error.request) {
      Message({
        message: JSON.parse(error.request.response).message,
        type: 'error',
        duration: 5 * 1000
      })
    } else if (error.response) {
      Message({
        message: JSON.parse(error.response.response).message,
        type: 'error',
        duration: 5 * 1000
      })
    }
    return Promise.reject(error)
  }
)

export default service
