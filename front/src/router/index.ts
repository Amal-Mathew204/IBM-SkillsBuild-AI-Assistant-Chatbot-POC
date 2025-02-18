import { createRouter, createWebHistory } from 'vue-router'
import ChatbotSettings from '../components/Settings.vue';
import ChatBot from '../components/ChatBot.vue';
import DataScience from '@/components/DataScience.vue';

const routes = [
  { path: '/settings', name: 'Settings', component: ChatbotSettings },
  { path: '/', name: 'ChatBot', component: ChatBot }, 
  { path: '/datascience', name: 'DataScience', component: DataScience },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
})

export default router
