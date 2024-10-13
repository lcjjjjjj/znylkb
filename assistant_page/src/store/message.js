const state = {
    sendMessage: []
}

const mutations = {
    addMsg (state, payload) {
        state.sendMessage.push(payload)
    },
    clearMsg (state) {
        state.sendMessage = []
    }
}

export default {
    state,
    mutations
}