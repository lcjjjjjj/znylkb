import { createStore } from "vuex";
import menu from "./menu";
import message from "./message";
import user from "./user";

export default createStore({
    modules: {
        menu,
        message,
        user
    }
})