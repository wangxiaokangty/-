//导入vue-router
import { createRouter, createWebHistory } from 'vue-router'
//导入组件
import PostTaskView from "@/views/PostTaskView.vue"
import TaskMarketView from "@/views/TaskMarketView.vue"
import PersonInfoView from "@/views/MyPersonInfoView.vue";
import UserLoginView from "@/views/UserLoginView.vue";
import HomeView from "@/views/HomeView.vue";
import MyPostedTaskView from "@/views/MyPostedTaskView.vue";
import MyWorkView from "@/views/MyWorkView.vue";
import TaskDetailView from "@/views/TaskDetailView.vue";
import AdminTaskView from "@/views/AdminTaskView.vue";
import AdminReportView from "@/views/AdminReportView.vue";
//定义路由关系
const routes = [
    { path: '/', name:'',component: UserLoginView},
    { path: '/login', name:'login',component: UserLoginView },
    { path: '/home', name:'home',component: HomeView },
    { path: '/post-task', name:'post-task',component: PostTaskView },
    { path: '/task-market', name:'task-market',component: TaskMarketView },
    { path: '/personal-info', name:'personal-info',component: PersonInfoView },
    { path: '/posted-tasks', name:'posted-tasks',component: MyPostedTaskView },
    { path: '/tasks-to-complete', name:'tasks-to-complete',component: MyWorkView },
    {
        path: '/task-detail/:task_id', // 动态路由，`taskId` 是一个动态参数
        name: 'task-detail',
        component: TaskDetailView, // 假设您有一个名为 UserProfileView 的组件
    },
    { path: '/admin-task', name: 'admin-task', component: AdminTaskView,},
    { path: '/admin-report', name:'admin-report',component: AdminReportView },
]

//创建路由器
const router = createRouter({
    history: createWebHistory(),
    routes: routes
});

export default router