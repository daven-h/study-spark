import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { Task } from '@/types/task';

interface TaskState {
  tasks: Task[];
  addTask: (title: string, estimatePomos?: number) => void;
  toggleTask: (id: string) => void;
  deleteTask: (id: string) => void;
  updateTask: (id: string, updates: Partial<Task>) => void;
}

export const useTaskStore = create<TaskState>()(
  persist(
    (set) => ({
      tasks: [],
      
      addTask: (title, estimatePomos) => set((state) => ({
        tasks: [
          ...state.tasks,
          {
            id: crypto.randomUUID(),
            title,
            estimatePomos,
            done: false,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
          }
        ]
      })),
      
      toggleTask: (id) => set((state) => ({
        tasks: state.tasks.map(task =>
          task.id === id 
            ? { ...task, done: !task.done, updatedAt: new Date().toISOString() }
            : task
        )
      })),
      
      deleteTask: (id) => set((state) => ({
        tasks: state.tasks.filter(task => task.id !== id)
      })),
      
      updateTask: (id, updates) => set((state) => ({
        tasks: state.tasks.map(task =>
          task.id === id 
            ? { ...task, ...updates, updatedAt: new Date().toISOString() }
            : task
        )
      })),
    }),
    {
      name: 'task-storage',
    }
  )
);