from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user

from .models import Question, Answer


class SignUpPageTest(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'A9q5W1z7S5xE3d'

    def test_register_page(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='qr/register.html')

    def test_register_form(self):
        response = self.client.post(reverse('qr:register'), data={
            'username': self.username,
            'password1': self.password,
            'password2': self.password
        })
        self.assertRedirects(response, '/login/')

        users = User.objects.all()
        self.assertEqual(users.count(), 1)


class LoginPageTest(TestCase):
    def setUp(self):
        self.credentials = {'username': 'testuser', 'password': 'testpassword'}
        User.objects.create_user(**self.credentials)

    def test_login_page(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='qr/login.html')

    def test_user_is_logged_in(self):
        self.assertTrue(self.client.login(username='testuser', password='testpassword'))

    def test_user_is_not_logged_in(self):
        self.assertFalse(self.client.login(username='testuser', password='fdhdgfhhb'))

    def test_user_is_redirected(self):
        response = self.client.post(reverse('qr:login'), data=self.credentials)
        self.assertRedirects(response, reverse('qr:index'))


class LogoutPageTest(TestCase):
    def test_user_is_logged_out(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.client.logout()
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout_redirect(self):
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/login/")


class IndexPageTest(TestCase):
    def test_index_page(self):
        """Test that index page return 200"""
        response = self.client.get(reverse('qr:index'))
        self.assertEqual(response.status_code, 200)


class AskQuestionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_ask_question_page(self):
        response = self.client.get(reverse('qr:ask_question'))
        self.assertEqual(response.status_code, 200)

    def test_question_form(self):
        response = self.client.post(reverse('qr:ask_question'), data={
            'topic': "This is a test question",
            'description': "This is the description",
        })
        self.question = Question.objects.get(topic="This is a test question")
        self.assertRedirects(response, reverse('qr:detail', args=(self.question.id,)))

        questions = Question.objects.all()
        self.assertEqual(questions.count(), 1)


class DetailPageTest(TestCase):
    "Tests for detail page (= page displaying a question + answers + answer form)"
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.question = Question.objects.create(topic="This is a test question", user=self.user)

    def test_detail_page_returns_200(self):
        question_id = self.question.id
        response = self.client.get(reverse('qr:detail', args=(question_id,)))
        self.assertEqual(response.status_code, 200)

    def test_detail_page_returns_404(self):
        question_id = self.question.id + 1
        response = self.client.get(reverse('qr:detail', args=(question_id,)))
        self.assertEqual(response.status_code, 404)

    def test_answer_form(self):
        response = self.client.post(reverse('qr:detail', args=(self.question.id,)), data={
            'reply': "This is a test answer",
        })
        self.answer = Answer.objects.get(reply="This is a test answer")
        self.assertRedirects(response, reverse('qr:detail', args=(self.question.id,)))

        answers = Answer.objects.all()
        self.assertEqual(answers.count(), 1)

    def test_edit_question(self):
        Question.objects.filter(pk=self.question.pk).update(topic="This is a test question 2 ? [edited]")
        self.question.refresh_from_db()
        self.assertEqual(self.question.topic, "This is a test question 2 ? [edited]")

    def test_delete_question(self):
        Question.objects.filter(pk=self.question.pk).delete()
        self.assertEqual(Question.objects.all().count(), 0)

    def test_edit_answer(self):
        self.answer = Answer.objects.create(reply="This is a test answer.", user=self.user)
        Answer.objects.filter(pk=self.answer.pk).update(reply="This is a test answer.[edited]")
        self.answer.refresh_from_db()
        self.assertEqual(self.answer.reply, "This is a test answer.[edited]")

    def test_delete_answer(self):
        self.answer = Answer.objects.create(reply="This is a test answer.", user=self.user)
        Answer.objects.filter(pk=self.answer.pk).delete()
        self.assertEqual(Answer.objects.all().count(), 0)


class ProfilePageTest(TestCase):
    def test_profile_page(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('qr:profile'))
        self.assertEqual(response.status_code, 200)

    def test_no_profile_page(self):
        response = self.client.get(reverse('qr:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/profile/')
