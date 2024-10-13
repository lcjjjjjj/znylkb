const state = {
    userInfo: []
}

const mutations = {
    addInfo (state, payload) {
        state.userInfo.push(payload)
    },
    clearInfo (state) {
        state.userInfo = []
    }
}

export default {
    state,
    mutations
}