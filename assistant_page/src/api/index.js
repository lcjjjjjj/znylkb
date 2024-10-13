import request from '../utils/request'

export const postText = (data) => {
    return request.post('/textsum',data)
}

export const postSignal = (data) => {
    return request.post('/rtasr',data)
}

export const postKeep = (data) => {
    return request.post('/result',data)
}

export const postClear = (data) => {
    return request.post('/clear',data)
}

export const getFile = (params) => {
    return request.get('/download',{params, responseType: 'blob'})
}

export const deleteFile = () => {
    return request.delete('/delete')
}

export const getFilelist = (data) => {
    return request.get('/getfilelist',{params: data})
}

export const userOption = (data) => {
    return request.post('/useroption', data)
}

export const userUpdate = (data) => {
    return request.post('/userupdate', data)
}