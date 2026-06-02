import 'package:flutter/material.dart';

void main() {
  // TODO: Initialize Firebase after running `flutterfire configure`.
  // await Firebase.initializeApp(options: DefaultFirebaseOptions.currentPlatform);
  runApp(const CareerSyncApp());
}

class CareerSyncApp extends StatelessWidget {
  const CareerSyncApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'CareerSync AI',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF0F766E)),
        useMaterial3: true,
        scaffoldBackgroundColor: const Color(0xFFF6F8FB),
      ),
      home: const LoginScreen(),
    );
  }
}

class Exam {
  const Exam(this.name, this.type, this.date, this.progress, this.topics);

  final String name;
  final String type;
  final String date;
  final int progress;
  final List<String> topics;
}

const exams = [
  Exam('AptiReady Test', 'Aptitude', '15 Jul 2026', 68, ['Percentages', 'Reasoning', 'Verbal ability']),
  Exam('CodeStart Test', 'Basic Coding', '22 Jul 2026', 74, ['Loops', 'Arrays', 'Strings']),
  Exam('CodePro Test', 'Advanced Coding', '05 Aug 2026', 42, ['Big O', 'Trees', 'Dynamic programming']),
];

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.psychology_alt, size: 48, color: Color(0xFF0F766E)),
              const SizedBox(height: 20),
              const Text('CareerSync AI', style: TextStyle(fontSize: 34, fontWeight: FontWeight.w800)),
              const SizedBox(height: 8),
              const Text('Prepare for mandatory IT readiness exams with focused materials and AI-guided practice.'),
              const SizedBox(height: 28),
              FilledButton.icon(
                onPressed: () => Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const HomeScreen())),
                icon: const Icon(Icons.login),
                label: const Text('Continue with Demo Login'),
              ),
              const SizedBox(height: 16),
              const Text('Firebase Auth placeholder is ready. Add config before production login.'),
            ],
          ),
        ),
      ),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int index = 0;

  @override
  Widget build(BuildContext context) {
    final pages = [
      const DashboardScreen(),
      const ResumeScreen(),
      const InterviewScreen(),
      const ProfileScreen(),
    ];
    return Scaffold(
      appBar: AppBar(title: const Text('CareerSync AI')),
      body: pages[index],
      bottomNavigationBar: NavigationBar(
        selectedIndex: index,
        onDestinationSelected: (value) => setState(() => index = value),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.dashboard_outlined), selectedIcon: Icon(Icons.dashboard), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.description_outlined), selectedIcon: Icon(Icons.description), label: 'Resume'),
          NavigationDestination(icon: Icon(Icons.school_outlined), selectedIcon: Icon(Icons.school), label: 'Interview'),
          NavigationDestination(icon: Icon(Icons.person_outline), selectedIcon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }
}

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        const Text('Your IT readiness plan', style: TextStyle(fontSize: 26, fontWeight: FontWeight.w800)),
        const SizedBox(height: 16),
        const Wrap(
          spacing: 12,
          runSpacing: 12,
          children: [
            MetricCard(label: 'Resume score', value: '78%'),
            MetricCard(label: 'Mock interviews', value: '4'),
            MetricCard(label: 'Progress', value: '61%'),
          ],
        ),
        const SizedBox(height: 16),
        for (final exam in exams) ExamCard(exam: exam),
      ],
    );
  }
}

class ResumeScreen extends StatelessWidget {
  const ResumeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: const [
        Text('AI Resume Analysis', style: TextStyle(fontSize: 26, fontWeight: FontWeight.w800)),
        SizedBox(height: 16),
        InfoCard(
          title: 'Upload Resume',
          body: 'Connect file picker and POST /api/resume/upload/ in the next version.',
          icon: Icons.upload_file,
        ),
        InfoCard(
          title: 'Mock Feedback',
          body: 'Score: 78%. Add measurable project outcomes, group skills clearly, and mention exam readiness.',
          icon: Icons.auto_awesome,
        ),
      ],
    );
  }
}

class InterviewScreen extends StatelessWidget {
  const InterviewScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final questions = [
      'Why do you want an IT role?',
      'Explain a coding problem you solved recently.',
      'How do you manage time in aptitude tests?',
      'What is the difference between stack and queue?',
    ];
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        const Text('Interview Questions', style: TextStyle(fontSize: 26, fontWeight: FontWeight.w800)),
        const SizedBox(height: 16),
        for (final question in questions)
          Card(
            child: ListTile(
              leading: const Icon(Icons.question_answer_outlined),
              title: Text(question),
            ),
          ),
      ],
    );
  }
}

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        const Text('Profile', style: TextStyle(fontSize: 26, fontWeight: FontWeight.w800)),
        const SizedBox(height: 16),
        const TextField(decoration: InputDecoration(labelText: 'Name', border: OutlineInputBorder())),
        const SizedBox(height: 12),
        const TextField(decoration: InputDecoration(labelText: 'Target role', border: OutlineInputBorder())),
        const SizedBox(height: 12),
        const TextField(decoration: InputDecoration(labelText: 'Skills', border: OutlineInputBorder())),
        const SizedBox(height: 16),
        FilledButton(
          onPressed: () => ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Profile saved in demo mode')),
          ),
          child: const Text('Save Profile'),
        ),
      ],
    );
  }
}

class MetricCard extends StatelessWidget {
  const MetricCard({super.key, required this.label, required this.value});

  final String label;
  final String value;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 150,
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(label),
              const SizedBox(height: 8),
              Text(value, style: const TextStyle(fontSize: 26, fontWeight: FontWeight.w800)),
            ],
          ),
        ),
      ),
    );
  }
}

class ExamCard extends StatelessWidget {
  const ExamCard({super.key, required this.exam});

  final Exam exam;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(exam.type, style: const TextStyle(color: Color(0xFF0F766E), fontWeight: FontWeight.w800)),
            Text(exam.name, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w800)),
            Text('Next window: ${exam.date}'),
            const SizedBox(height: 10),
            LinearProgressIndicator(value: exam.progress / 100),
            const SizedBox(height: 10),
            Text(exam.topics.join(' • ')),
          ],
        ),
      ),
    );
  }
}

class InfoCard extends StatelessWidget {
  const InfoCard({super.key, required this.title, required this.body, required this.icon});

  final String title;
  final String body;
  final IconData icon;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        leading: Icon(icon, color: const Color(0xFF0F766E)),
        title: Text(title),
        subtitle: Text(body),
      ),
    );
  }
}
