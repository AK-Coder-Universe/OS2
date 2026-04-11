import os
import re

files = [f for f in os.listdir('.') if f.endswith('.pdf')]
slips = {}
for f in files:
    m = re.match(r'slip(\d+)q(\d+)\.pdf', f, re.IGNORECASE)
    if m:
        slip_no = int(m.group(1))
        q_no = int(m.group(2))
        if slip_no not in slips:
            slips[slip_no] = []
        slips[slip_no].append({'q_no': q_no, 'filename': f})

html_parts = []
html_parts.append('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OS Slip Solutions (1 to 30)</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0f172a;
            --surface-color: #1e293b;
            --primary-color: #3b82f6;
            --primary-hover: #2563eb;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #10b981;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }
        
        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        header {
            background: rgba(30, 41, 59, 0.8);
            backdrop-filter: blur(12px);
            padding: 2rem;
            text-align: center;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            position: sticky;
            top: 0;
            z-index: 10;
        }

        header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        
        header p {
            color: var(--text-muted);
            font-size: 1.1rem;
        }

        main {
            padding: 3rem;
            flex: 1;
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
        }

        .slip-card {
            background: var(--surface-color);
            border-radius: 16px;
            padding: 1.5rem;
            border: 1px solid rgba(255,255,255,0.05);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }

        .slip-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            border-color: rgba(59, 130, 246, 0.5);
        }

        .slip-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(to bottom, #3b82f6, #8b5cf6);
            border-radius: 4px 0 0 4px;
        }

        .slip-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1.2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .slip-title span.badge {
            background: rgba(59, 130, 246, 0.1);
            color: #60a5fa;
            font-size: 0.8rem;
            padding: 0.3rem 0.6rem;
            border-radius: 999px;
            font-weight: 500;
        }

        .questions {
            display: flex;
            gap: 0.8rem;
            flex-wrap: wrap;
        }

        .question-btn {
            background: rgba(255,255,255,0.05);
            color: var(--text-main);
            text-decoration: none;
            padding: 0.6rem 1rem;
            border-radius: 8px;
            font-weight: 500;
            font-size: 0.95rem;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            border: 1px solid rgba(255,255,255,0.1);
            cursor: pointer;
        }

        .question-btn:hover {
            background: var(--primary-color);
            border-color: var(--primary-color);
            color: white;
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.4);
        }

        /* Modal styling */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(8px);
            z-index: 100;
            display: none;
            opacity: 0;
            transition: opacity 0.3s;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }

        .modal-overlay.active {
            display: flex;
            opacity: 1;
        }

        .modal-content {
            background: var(--surface-color);
            width: 100%;
            max-width: 1200px;
            height: 90vh;
            border-radius: 16px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transform: scale(0.95);
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }

        .modal-overlay.active .modal-content {
            transform: scale(1);
        }

        .modal-header {
            padding: 1.2rem 2rem;
            background: rgba(15, 23, 42, 0.9);
            border-bottom: 1px solid rgba(255,255,255,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .modal-title {
            font-size: 1.3rem;
            font-weight: 600;
        }

        .close-btn {
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 1.5rem;
            cursor: pointer;
            transition: color 0.2s;
            padding: 0.5rem;
            line-height: 1;
        }

        .close-btn:hover {
            color: #ef4444;
        }

        .modal-body {
            flex: 1;
            background: #e2e8f0;
        }

        .modal-body iframe {
            width: 100%;
            height: 100%;
            border: none;
        }

        .empty-state {
            text-align: center;
            padding: 4rem;
            color: var(--text-muted);
            font-size: 1.2rem;
        }
        
        .footer {
            text-align: center;
            padding: 2rem;
            color: var(--text-muted);
            font-size: 0.9rem;
            border-top: 1px solid rgba(255,255,255,0.05);
            margin-top: 2rem;
        }
    </style>
</head>
<body>

    <header>
        <h1>Operating System Lab Slips</h1>
        <p>Interactive dashboard to view all available PDF solutions (Slips 1-30)</p>
        <div style="margin-top: 1.5rem;">
            <button class="question-btn" style="display: inline-flex; align-items: center; justify-content: center; background: var(--primary-color); color: white; padding: 0.8rem 1.5rem; font-size: 1.1rem; border-radius: 8px; border: none; cursor: pointer; box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.5); transition: all 0.2s;" onmouseover="this.style.background=\'var(--primary-hover)\'; this.style.transform=\'translateY(-2px)\'" onmouseout="this.style.background=\'var(--primary-color)\'; this.style.transform=\'translateY(0)\'" onclick="openPdf(\'T.Y.B.Sc. CS-367 Operating System Practical Slips Sem VI (1).pdf\', \'All Questions\')">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 8px;">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                    <line x1="16" y1="13" x2="8" y2="13"></line>
                    <line x1="16" y1="17" x2="8" y2="17"></line>
                    <polyline points="10 9 9 9 8 9"></polyline>
                </svg>
                View All Questions PDF
            </button>
        </div>
    </header>

    <main>
        <div class="grid">
''')

# Create a full 1 to 30 range
for i in range(1, 31):
    html_parts.append(f'<div class="slip-card">')
    
    if i in slips:
        count = len(slips[i])
        html_parts.append(f'<div class="slip-title">Slip {i} <span class="badge">{count} PDF{"s" if count > 1 else ""}</span></div>')
        html_parts.append('<div class="questions">')
        # Sort by q_no
        slips[i].sort(key=lambda x: x['q_no'])
        for q in slips[i]:
            fname = q['filename']
            qno = q['q_no']
            label = f'Question {qno}'
            # Adding onclick event to open modal
            html_parts.append(f'<button class="question-btn" onclick="openPdf(\'{fname}\', \'Slip {i} - Question {qno}\')">')
            html_parts.append(f'''
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
                <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
            {label}
            </button>''')
        html_parts.append('</div>')
    else:
        html_parts.append(f'<div class="slip-title" style="color: var(--text-muted)">Slip {i} <span class="badge" style="background: rgba(255,255,255,0.05); color: var(--text-muted);">Missing</span></div>')
        html_parts.append('<div class="questions"><span style="color: var(--text-muted); font-size: 0.9rem;">No PDFs found</span></div>')
        
    html_parts.append('</div>')

html_parts.append('''
        </div>
    </main>

    <div class="footer">
        Generated for OS Lab Answers | Slip Questions 1 to 30
    </div>

    <!-- PDF Viewer Modal -->
    <div class="modal-overlay" id="pdfModal">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title" id="modalTitle">PDF Viewer</div>
                <button class="close-btn" onclick="closePdf()">&times;</button>
            </div>
            <div class="modal-body">
                <!-- Fallback link in case iframe does not render nicely for local files in some browsers -->
                <div id="fallbackLink" style="padding: 1rem; background: #f1f5f9; color: #334155; text-align: center; border-bottom: 1px solid #cbd5e1; display: none;">
                    If the PDF doesn't display below, <a id="directLink" href="#" target="_blank" style="color: #2563eb; font-weight: 600;">Click here to open it directly</a>.
                </div>
                <iframe id="pdfIframe" src=""></iframe>
            </div>
        </div>
    </div>

    <script>
        const modal = document.getElementById('pdfModal');
        const iframe = document.getElementById('pdfIframe');
        const modalTitle = document.getElementById('modalTitle');
        const fallbackLink = document.getElementById('fallbackLink');
        const directLink = document.getElementById('directLink');

        function openPdf(filename, title) {
            modalTitle.textContent = title;
            iframe.src = filename;
            directLink.href = filename;
            fallbackLink.style.display = 'block';
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function closePdf() {
            modal.classList.remove('active');
            setTimeout(() => {
                iframe.src = '';
            }, 300);
            document.body.style.overflow = '';
        }

        // Close modal on clicking outside
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closePdf();
            }
        });

        // Close on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.classList.contains('active')) {
                closePdf();
            }
        });
    </script>
</body>
</html>
''')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write('\n'.join(html_parts))

print("HTML successfully generated!")
