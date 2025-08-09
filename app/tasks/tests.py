from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Task

User = get_user_model()

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_create_task(self):
        task = Task.objects.create(content='Test task', user=self.user)
        self.assertEqual(task.content, 'Test task')
        self.assertFalse(task.is_completed)
        self.assertEqual(task.user, self.user)

class TaskViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_task_list_view(self):
        response = self.client.get(reverse('tasks:task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')

    def test_task_create_view(self):
        response = self.client.post(reverse('tasks:task-create'), {
            'content': 'Nueva tarea',
            'is_completed': False
        })
        self.assertEqual(response.status_code, 302)  # Redirige tras crear
        self.assertTrue(Task.objects.filter(content='Nueva tarea').exists())

    def test_task_toggle_complete_view(self):
        task = Task.objects.create(content='Tarea toggle', user=self.user)
        response = self.client.post(reverse('tasks:task-toggle-complete', args=[task.id]))
        task.refresh_from_db()
        self.assertTrue(task.is_completed)

    def test_task_delete_view(self):
        task = Task.objects.create(content='Tarea borrar', user=self.user)
        response = self.client.post(reverse('tasks:task-delete', args=[task.id]))
        self.assertFalse(Task.objects.filter(id=task.id).exists())

class TaskAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='apitest', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_api_create_task(self):
        response = self.client.post('/api/tasks/', {'content': 'API tarea'})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Task.objects.filter(content='API tarea').exists())

    def test_api_list_tasks(self):
        Task.objects.create(content='API tarea 2', user=self.user)
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)

    def test_api_toggle_complete(self):
        task = Task.objects.create(content='API toggle', user=self.user)
        response = self.client.put(f'/api/tasks/{task.id}/toggle_complete/')
        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertTrue(task.is_completed)

    def test_api_delete_task(self):
        task = Task.objects.create(content='API borrar', user=self.user)
        response = self.client.delete(f'/api/tasks/{task.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Task.objects.filter(id=task.id).exists())