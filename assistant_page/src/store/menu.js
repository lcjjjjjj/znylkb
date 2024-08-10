const state = {
    isCollapsed: false, // 是否折叠
    selectMenu: []
}

const mutations = {
    collapseMenu (state) {
        state.isCollapsed = !state.isCollapsed
    },
    addMenu (state, payload) {
        //需要对数据进行去重
        if(state.selectMenu.findIndex((item) => item.path === payload.path) === -1){
            state.selectMenu.push(payload)
        }
    },
    closeMenu (state, payload) {
        //找到点击的Tab的索引
        const index = state.selectMenu.findIndex((item) => item.name === payload.name)
        //通过索引删除
        state.selectMenu.splice(index, 1)
    }
}

export default {
    state,
    mutations
}