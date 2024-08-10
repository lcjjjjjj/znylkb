import axios from "axios";
import { ElMessage } from "element-plus";

const http = axios.create({
    baseURL: "http://localhost:5000",
    timeout: 10000,
    headers: {'Content-Type': 'application/json'}
})

export default http