


from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Docs"])


@router.get(
    "/api-docs",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def api_docs():
    return """
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <title>DeepAgent Course Generator API Docs</title>
        <style>
          body { font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; line-height: 1.6; padding: 0 20px; }
          code, pre { background: #f5f5f5; padding: 2px 6px; border-radius: 4px; }
          pre { padding: 16px; overflow: auto; }
        </style>
      </head>
      <body>
        <h1>DeepAgent Course Generator API Docs</h1>
        <p>Interactive documentation is available at <code>/docs</code> and <code>/redoc</code>.</p>
        <h2>Endpoints</h2>
        <ul>
          <li><code>GET /health</code> - health check for DB, Crawl4AI, SearXNG, and LLM</li>
          <li><code>POST /courses/generate</code> - generate a structured course from a prompt</li>
        </ul>
      </body>
    </html>
    """


@router.get(
    "/",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def home_page():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DeepAgent Course Studio</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        :root {
            --bg-dark: #090d16;
            --card-bg: rgba(17, 24, 39, 0.7);
            --card-border: rgba(255, 255, 255, 0.06);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-primary: #6366f1;
            --accent-secondary: #a855f7;
            --accent-gradient: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
            --accent-glow: rgba(99, 102, 241, 0.15);
            --hover-border: rgba(99, 102, 241, 0.4);
            --font-main: 'Inter', sans-serif;
            --font-display: 'Outfit', sans-serif;
            --sidebar-width: 380px;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: var(--font-main);
            background-color: var(--bg-dark);
            color: var(--text-primary);
            overflow: hidden;
            height: 100vh;
            display: flex;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(168, 85, 247, 0.08) 0%, transparent 40%);
        }

        /* App Container */
        .app-container {
            display: flex;
            width: 100vw;
            height: 100vh;
        }

        /* Sidebar Styling */
        .sidebar {
            width: var(--sidebar-width);
            background: rgba(10, 15, 28, 0.85);
            border-right: 1px solid var(--card-border);
            backdrop-filter: blur(20px);
            display: flex;
            flex-direction: column;
            height: 100%;
            flex-shrink: 0;
        }

        .sidebar-header {
            padding: 24px;
            border-bottom: 1px solid var(--card-border);
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo-icon {
            width: 36px;
            height: 36px;
            background: var(--accent-gradient);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        }

        .logo-text {
            font-family: var(--font-display);
            font-size: 20px;
            font-weight: 700;
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }

        /* Generator Section */
        .generator-box {
            padding: 24px;
            border-bottom: 1px solid var(--card-border);
        }

        .generator-box h3 {
            font-family: var(--font-display);
            font-size: 15px;
            font-weight: 600;
            margin-bottom: 12px;
            color: var(--text-primary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .input-wrapper {
            position: relative;
        }

        .prompt-input {
            width: 100%;
            height: 100px;
            background: rgba(17, 24, 39, 0.6);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 12px 16px;
            color: var(--text-primary);
            font-family: var(--font-main);
            font-size: 14px;
            resize: none;
            outline: none;
            transition: all 0.3s ease;
        }

        .prompt-input:focus {
            border-color: var(--accent-primary);
            box-shadow: 0 0 15px var(--accent-glow);
            background: rgba(17, 24, 39, 0.8);
        }

        .generate-btn {
            width: 100%;
            margin-top: 12px;
            padding: 12px;
            border: none;
            border-radius: 12px;
            background: var(--accent-gradient);
            color: #fff;
            font-family: var(--font-display);
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        }

        .generate-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5);
        }

        .generate-btn:active {
            transform: translateY(0);
        }

        /* Course List Section */
        .course-list-container {
            flex-grow: 1;
            overflow-y: auto;
            padding: 24px;
        }

        .course-list-container h3 {
            font-family: var(--font-display);
            font-size: 15px;
            font-weight: 600;
            margin-bottom: 16px;
            color: var(--text-primary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .course-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .course-card {
            background: rgba(17, 24, 39, 0.4);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .course-card:hover {
            background: rgba(17, 24, 39, 0.7);
            border-color: var(--hover-border);
            transform: translateY(-2px);
        }

        .course-card.active {
            background: rgba(99, 102, 241, 0.1);
            border-color: var(--accent-primary);
            box-shadow: 0 0 10px rgba(99, 102, 241, 0.1);
        }

        .course-card-category {
            font-size: 11px;
            text-transform: uppercase;
            font-weight: 700;
            color: var(--accent-primary);
            margin-bottom: 4px;
            letter-spacing: 0.5px;
        }

        .course-card-title {
            font-family: var(--font-display);
            font-size: 15px;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 6px;
            line-height: 1.3;
        }

        .course-card-desc {
            font-size: 12px;
            color: var(--text-secondary);
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            line-height: 1.4;
        }

        .course-card-meta {
            margin-top: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 11px;
            color: var(--text-secondary);
        }

        /* Main Workspace Section */
        .main-workspace {
            flex-grow: 1;
            height: 100%;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        /* Empty & Loading States */
        .workspace-empty, .workspace-loading {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 40px;
            text-align: center;
        }

        .empty-illustration {
            width: 180px;
            height: 180px;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 70%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 24px;
        }

        .empty-illustration svg {
            width: 80px;
            height: 80px;
            fill: none;
            stroke: var(--accent-primary);
            stroke-width: 1.5;
        }

        .workspace-empty h2 {
            font-family: var(--font-display);
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 12px;
        }

        .workspace-empty p {
            color: var(--text-secondary);
            max-width: 480px;
            font-size: 15px;
            line-height: 1.6;
        }

        /* Loading Spinner */
        .spinner {
            width: 60px;
            height: 60px;
            border: 4px solid rgba(255, 255, 255, 0.05);
            border-top: 4px solid var(--accent-primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 24px;
            box-shadow: 0 0 20px var(--accent-glow);
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .workspace-loading h2 {
            font-family: var(--font-display);
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 12px;
        }

        .progress-steps {
            display: flex;
            flex-direction: column;
            gap: 16px;
            margin-top: 30px;
            align-items: flex-start;
            max-width: 400px;
            width: 100%;
            background: rgba(17, 24, 39, 0.5);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 24px;
        }

        .progress-step {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 14px;
            color: var(--text-secondary);
        }

        .progress-step-icon {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            border: 2px solid var(--card-border);
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }

        .progress-step.active {
            color: var(--text-primary);
            font-weight: 600;
        }

        .progress-step.active .progress-step-icon {
            border-color: var(--accent-primary);
            background: var(--accent-primary);
            box-shadow: 0 0 10px rgba(99, 102, 241, 0.5);
        }

        .progress-step.completed {
            color: #10b981;
        }

        .progress-step.completed .progress-step-icon {
            border-color: #10b981;
            background: #10b981;
        }

        /* Course Dashboard Layout */
        .course-viewer {
            display: flex;
            flex-grow: 1;
            height: 100%;
            overflow: hidden;
        }

        /* Course Navigation (Chapters/Lessons Sidebar inside Content View) */
        .course-nav-sidebar {
            width: 320px;
            background: rgba(10, 15, 28, 0.5);
            border-right: 1px solid var(--card-border);
            overflow-y: auto;
            padding: 24px;
            flex-shrink: 0;
        }

        .chapter-container {
            margin-bottom: 20px;
        }

        .chapter-header {
            font-family: var(--font-display);
            font-size: 13px;
            font-weight: 700;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            padding-left: 8px;
        }

        .lesson-list {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .lesson-item {
            padding: 10px 14px;
            border-radius: 8px;
            font-size: 13.5px;
            color: var(--text-secondary);
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .lesson-item:hover {
            background: rgba(255, 255, 255, 0.03);
            color: var(--text-primary);
        }

        .lesson-item.active {
            background: rgba(99, 102, 241, 0.15);
            color: var(--text-primary);
            font-weight: 500;
        }

        /* Content Area */
        .course-content-area {
            flex-grow: 1;
            overflow-y: auto;
            padding: 40px 60px;
            background: rgba(15, 23, 42, 0.15);
        }

        /* Metadata Banner */
        .course-banner {
            border-bottom: 1px solid var(--card-border);
            padding: 30px 40px;
            background: rgba(10, 15, 28, 0.3);
            backdrop-filter: blur(10px);
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }

        .banner-left h1 {
            font-family: var(--font-display);
            font-size: 26px;
            font-weight: 800;
            margin-bottom: 8px;
            background: linear-gradient(to right, #ffffff, #cbd5e1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .banner-left p {
            color: var(--text-secondary);
            font-size: 14px;
        }

        .badge {
            background: var(--accent-gradient);
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: inline-block;
            margin-bottom: 10px;
        }

        .banner-right {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 8px;
        }

        .meta-stat {
            font-size: 12px;
            color: var(--text-secondary);
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--card-border);
            padding: 6px 12px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* Markdown Content Styling */
        .markdown-body {
            max-width: 800px;
            margin: 0 auto;
            line-height: 1.7;
            font-size: 15px;
            color: #cbd5e1;
        }

        .markdown-body h1, .markdown-body h2, .markdown-body h3, .markdown-body h4 {
            font-family: var(--font-display);
            color: var(--text-primary);
            margin-top: 32px;
            margin-bottom: 16px;
            font-weight: 700;
        }

        .markdown-body h1 { font-size: 28px; border-bottom: 1px solid var(--card-border); padding-bottom: 8px; }
        .markdown-body h2 { font-size: 22px; }
        .markdown-body h3 { font-size: 18px; }

        .markdown-body p {
            margin-bottom: 18px;
        }

        .markdown-body code {
            font-family: monospace;
            background: rgba(255, 255, 255, 0.05);
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 14px;
            color: #f43f5e;
        }

        .markdown-body pre {
            background: rgba(10, 15, 28, 0.85);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 20px;
            overflow: auto;
            margin-bottom: 24px;
        }

        .markdown-body pre code {
            background: transparent;
            padding: 0;
            color: #e2e8f0;
            font-size: 13.5px;
        }

        .markdown-body ul, .markdown-body ol {
            margin-left: 24px;
            margin-bottom: 18px;
        }

        .markdown-body li {
            margin-bottom: 6px;
        }

        .markdown-body blockquote {
            border-left: 4px solid var(--accent-primary);
            background: rgba(99, 102, 241, 0.05);
            padding: 12px 20px;
            border-radius: 0 8px 8px 0;
            margin-bottom: 20px;
            font-style: italic;
        }

        .markdown-body table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 24px;
        }

        .markdown-body th, .markdown-body td {
            border: 1px solid var(--card-border);
            padding: 10px 14px;
            font-size: 14px;
            text-align: left;
        }

        .markdown-body th {
            background: rgba(255, 255, 255, 0.03);
            color: var(--text-primary);
            font-weight: 600;
        }

        /* Custom Scrollbars */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: transparent;
        }

        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.2);
        }
    </style>
</head>
<body>
    <div class="app-container">
        <!-- Sidebar -->
        <aside class="sidebar">
            <div class="sidebar-header">
                <div class="logo-icon">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2">
                        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                        <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                    </svg>
                </div>
                <div class="logo-text">DeepAgent Studio</div>
            </div>

            <!-- Generate Box -->
            <div class="generator-box">
                <h3>Generate Course</h3>
                <div class="input-wrapper">
                    <textarea id="promptInput" class="prompt-input" placeholder="e.g. Create a beginner course about Python programming..."></textarea>
                </div>
                <button id="generateBtn" class="generate-btn">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polygon points="5 3 19 12 5 21 5 3"></polygon>
                    </svg>
                    Create Course
                </button>
            </div>

            <!-- List of Courses -->
            <div class="course-list-container">
                <h3>My Library</h3>
                <div id="courseList" class="course-list">
                    <!-- Course cards dynamically added -->
                </div>
            </div>
        </aside>

        <!-- Main Workspace -->
        <main class="main-workspace">
            <!-- Empty state -->
            <div id="emptyState" class="workspace-empty">
                <div class="empty-illustration">
                    <svg viewBox="0 0 24 24">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                </div>
                <h2>No Course Selected</h2>
                <p>Choose an existing course from your library on the left or enter a prompt to generate a brand new interactive pathway using AI agents.</p>
            </div>

            <!-- Loading state -->
            <div id="loadingState" class="workspace-loading" style="display: none;">
                <div class="spinner"></div>
                <h2>Assembling Course...</h2>
                <p>Our agentic team is researching, selecting the template, and drafting content lesson-by-lesson. This process takes a few minutes.</p>
                <div class="progress-steps">
                    <div id="step-metadata" class="progress-step active">
                        <div class="progress-step-icon">1</div>
                        <span>Agent 1: Structuring metadata & requirements</span>
                    </div>
                    <div id="step-template" class="progress-step">
                        <div class="progress-step-icon">2</div>
                        <span>Agent 2: Selecting matching curriculum template</span>
                    </div>
                    <div id="step-content" class="progress-step">
                        <div class="progress-step-icon">3</div>
                        <span>Agent 3: Sequential lesson-by-lesson search & write</span>
                    </div>
                </div>
            </div>

            <!-- Course Dashboard (shown when a course is loaded) -->
            <div id="courseViewer" class="course-viewer" style="display: none;">
                <!-- Internal Sidebar for Lessons -->
                <nav id="lessonsSidebar" class="course-nav-sidebar">
                    <!-- Chapters & Lessons dynamically populated -->
                </nav>

                <!-- Reading Container -->
                <div class="main-workspace" style="flex-grow:1;">
                    <!-- Banner -->
                    <div class="course-banner">
                        <div class="banner-left">
                            <span id="courseCategory" class="badge">Programming</span>
                            <h1 id="courseTitle">Loading...</h1>
                            <p id="courseHeadline">Loading...</p>
                        </div>
                        <div class="banner-right">
                            <div id="courseDuration" class="meta-stat">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <circle cx="12" cy="12" r="10"></circle>
                                    <polyline points="12 6 12 12 16 14"></polyline>
                                </svg>
                                <span>-- hours</span>
                            </div>
                            <div id="courseLang" class="meta-stat">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                                </svg>
                                <span>English</span>
                            </div>
                        </div>
                    </div>

                    <!-- Lesson Reader -->
                    <div class="course-content-area">
                        <article id="markdownReader" class="markdown-body">
                            <!-- Lesson text rendered here -->
                        </article>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script>
        let coursesCache = [];
        let activeCourse = null;

        // Elements
        const promptInput = document.getElementById('promptInput');
        const generateBtn = document.getElementById('generateBtn');
        const courseList = document.getElementById('courseList');
        const emptyState = document.getElementById('emptyState');
        const loadingState = document.getElementById('loadingState');
        const courseViewer = document.getElementById('courseViewer');
        const lessonsSidebar = document.getElementById('lessonsSidebar');
        const courseTitle = document.getElementById('courseTitle');
        const courseHeadline = document.getElementById('courseHeadline');
        const courseCategory = document.getElementById('courseCategory');
        const courseDuration = document.getElementById('courseDuration');
        const courseLang = document.getElementById('courseLang');
        const markdownReader = document.getElementById('markdownReader');

        const stepMetadata = document.getElementById('step-metadata');
        const stepTemplate = document.getElementById('step-template');
        const stepContent = document.getElementById('step-content');

        // Fetch courses list on load
        async function loadCourses() {
            try {
                const res = await fetch('/courses');
                if (res.ok) {
                    coursesCache = await res.json();
                    renderCourseList();
                }
            } catch (err) {
                console.error("Failed to load courses:", err);
            }
        }

        // Render Sidebar Course List
        function renderCourseList() {
            courseList.innerHTML = '';
            if (coursesCache.length === 0) {
                courseList.innerHTML = '<p style="color: var(--text-secondary); font-size: 13px; text-align:center; padding: 20px 0;">No courses generated yet.</p>';
                return;
            }
            coursesCache.forEach(course => {
                const card = document.createElement('div');
                card.className = `course-card ${activeCourse && activeCourse.id === course.id ? 'active' : ''}`;
                card.onclick = () => selectCourse(course.id);

                const dateString = course.created_at ? new Date(course.created_at).toLocaleDateString() : '';

                card.innerHTML = `
                    <div class="course-card-category">${course.primary_subcategory_title || 'General'}</div>
                    <div class="course-card-title">${course.title}</div>
                    <div class="course-card-desc">${course.headline || ''}</div>
                    <div class="course-card-meta">
                        <span>${course.duration || '--'}</span>
                        <span>${dateString}</span>
                    </div>
                `;
                courseList.appendChild(card);
            });
        }

        // Select and Load Course
        async function selectCourse(id) {
            // Set states
            emptyState.style.display = 'none';
            loadingState.style.display = 'none';
            courseViewer.style.display = 'flex';

            // Show temporary loading indicator in banner/sidebar
            courseTitle.innerText = "Loading details...";
            markdownReader.innerHTML = "<p style='color: var(--text-secondary); text-align:center; margin-top:100px;'>Opening pathway...</p>";

            try {
                const res = await fetch(`/courses/${id}`);
                if (res.ok) {
                    activeCourse = await res.json();
                    
                    // Highlights in sidebar list
                    document.querySelectorAll('.course-card').forEach(el => el.classList.remove('active'));
                    renderCourseList();

                    displayCourse(activeCourse);
                }
            } catch (err) {
                console.error("Error loading course:", err);
            }
        }

        // Display Course in Dashboard
        function displayCourse(course) {
            courseCategory.innerText = course.primary_category_title || 'General';
            courseTitle.innerText = course.title;
            courseHeadline.innerText = course.headline;
            courseDuration.querySelector('span').innerText = course.duration || '--';
            courseLang.querySelector('span').innerText = course.language || 'English';

            // Build Lessons Navigation
            lessonsSidebar.innerHTML = '';
            const body = course.realcoursebody || {};
            const isChapters = 'chapters' in body;
            const items = isChapters ? body.chapters : body.sections;

            if (!items || items.length === 0) {
                lessonsSidebar.innerHTML = '<p style="color:var(--text-secondary);">No lessons found</p>';
                markdownReader.innerHTML = '<p style="color:var(--text-secondary);">This course has no contents generated.</p>';
                return;
            }

            let firstLesson = null;

            items.forEach((item, chIdx) => {
                const container = document.createElement('div');
                container.className = 'chapter-container';

                const header = document.createElement('div');
                header.className = 'chapter-header';
                header.innerText = `Ch ${chIdx + 1}: ${item.title}`;
                container.appendChild(header);

                const list = document.createElement('div');
                list.className = 'lesson-list';

                const lessons = item.lessons || [];
                lessons.forEach((lesson, lesIdx) => {
                    const itemEl = document.createElement('div');
                    itemEl.className = 'lesson-item';
                    itemEl.innerHTML = `
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                            <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                            <path d="M2 17l10 5 10-5"></path>
                            <path d="M2 12l10 5 10-5"></path>
                        </svg>
                        ${lesson.title}
                    `;
                    itemEl.onclick = () => selectLesson(lesson, itemEl);

                    if (!firstLesson) {
                        firstLesson = { lesson, element: itemEl };
                    }

                    list.appendChild(itemEl);
                });

                container.appendChild(list);
                lessonsSidebar.appendChild(container);
            });

            // Auto-select first lesson
            if (firstLesson) {
                selectLesson(firstLesson.lesson, firstLesson.element);
            }
        }

        // Render Lesson Markdown
        function selectLesson(lesson, element) {
            document.querySelectorAll('.lesson-item').forEach(el => el.classList.remove('active'));
            element.classList.add('active');

            if (lesson.content_markdown) {
                // If markdown doesn't start with a header, add one
                let md = lesson.content_markdown;
                if (!md.trim().startsWith('#')) {
                    md = `# ${lesson.title}\n\n` + md;
                }
                markdownReader.innerHTML = marked.parse(md);
            } else {
                markdownReader.innerHTML = `<h1>${lesson.title}</h1><p style='color:var(--text-secondary);'>No markdown content available for this lesson.</p>`;
            }
            // Scroll reader back to top
            document.querySelector('.course-content-area').scrollTop = 0;
        }

        // Generate Course
        generateBtn.onclick = async () => {
            const prompt = promptInput.value.trim();
            if (!prompt) return;

            // Reset UI States
            emptyState.style.display = 'none';
            courseViewer.style.display = 'none';
            loadingState.style.display = 'flex';
            generateBtn.disabled = true;
            generateBtn.style.opacity = '0.5';

            // Animate Loading Steps
            stepMetadata.className = 'progress-step active';
            stepTemplate.className = 'progress-step';
            stepContent.className = 'progress-step';

            setTimeout(() => {
                if (loadingState.style.display === 'flex') {
                    stepMetadata.className = 'progress-step completed';
                    stepTemplate.className = 'progress-step active';
                }
            }, 5000);

            setTimeout(() => {
                if (loadingState.style.display === 'flex') {
                    stepTemplate.className = 'progress-step completed';
                    stepContent.className = 'progress-step active';
                }
            }, 12000);

            try {
                const res = await fetch('/courses/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt })
                });

                if (res.ok) {
                    const course = await res.json();
                    promptInput.value = '';
                    
                    // Reload list
                    await loadCourses();
                    
                    // Load the newly generated course
                    selectCourse(course.id);
                } else {
                    alert("Generation failed. Check backend terminal for tool logs.");
                    emptyState.style.display = 'flex';
                    loadingState.style.display = 'none';
                }
            } catch (err) {
                console.error("Error generating course:", err);
                alert("Request error. Please make sure uvicorn is running.");
                emptyState.style.display = 'flex';
                loadingState.style.display = 'none';
            } finally {
                generateBtn.disabled = false;
                generateBtn.style.opacity = '1';
            }
        };

        // Initialize
        loadCourses();
    </script>
</body>
</html>
    """
