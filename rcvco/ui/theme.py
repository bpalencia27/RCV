import reflex as rx


def theme():
    return rx.html(
        """
        <style>
        /* Paleta accesible (AAA contrast > 7 en texto sobre bg) */
        :root {
            --bg-main:#f5f7fa;
            --bg-panel:#ffffff;
            --bg-panel-alt:#eef2f6;
            --bg-soft:#f0f3f8;
            --primary:#0d4abf;           /* Azul clínico principal */
            --primary-accent:#2563eb;     /* Azul acción */
            --primary-soft:#e0edff;       /* Fondo suave botones secundarios */
            --text-color:#1e2933;         /* Texto principal */
            --text-muted:#5b6773;         /* Texto secundario */
            --border-color:#d4dde6;       /* Bordes */
            --danger:#b91c1c;
            --warn:#b45309;
            --ok:#047857;
            --focus-ring:0 0 0 2px rgba(37,99,235,0.35);
            --radius-sm:4px; --radius-md:10px; --radius-lg:18px;
            --shadow-sm:0 1px 2px rgba(0,0,0,0.04),0 0 0 1px rgba(0,0,0,0.03);
            --shadow-md:0 4px 12px -2px rgba(0,0,0,0.08);
            --transition:120ms ease;
        }

        /* Modo oscuro */
        .dark-mode {
            --bg-main:#0f141a;
            --bg-panel:#18212b;
            --bg-panel-alt:#1f2a35;
            --bg-soft:#22313f;
            --text-color:#eef2f6;
            --text-muted:#9ca9b5;
            --border-color:#2d3b47;
            --primary:#3d82ff;
            --primary-accent:#3b82f6;
            --primary-soft:#123151;
            --focus-ring:0 0 0 2px rgba(61,130,255,0.5);
            --shadow-sm:0 1px 2px rgba(0,0,0,0.6),0 0 0 1px rgba(255,255,255,0.03);
            --shadow-md:0 4px 14px -2px rgba(0,0,0,0.55);
        }

        /* Alto contraste sobre-escribe (se puede combinar con dark) */
        .high-contrast {
            --primary:#0033dd;
            --primary-accent:#0033dd;
            --primary-soft:#dbe3ff;
            --border-color:#222;
            --text-muted:#333f49;
        }

        body { background:var(--bg-main); color:var(--text-color); font-family:'Segoe UI', system-ui, Arial, sans-serif; -webkit-font-smoothing:antialiased; }
        .main-grid { display:grid; grid-template-columns:1fr; min-height:100vh; }
        @media (min-width:1080px){ .main-grid { grid-template-columns:56% 44%; } }

        .form-panel { padding:2rem 2.25rem 4rem; background:var(--bg-panel); border-right:1px solid var(--border-color); height:100vh; overflow-y:auto; }
        .report-panel { padding:2rem 2.25rem 4rem; background:var(--bg-panel-alt); position:sticky; top:0; height:100vh; overflow-y:auto; }
        .report-panel .p-5 { background:var(--bg-panel); }

        h1,h2,h3,h4 { color:var(--text-color); letter-spacing:.5px; }
        .content { color:var(--text-muted); }

        .input-field { width:100%; border-radius:var(--radius-md); border:1px solid var(--border-color); padding:0.6rem 0.85rem; font-size:0.9rem; background:var(--bg-panel); color:var(--text-color); transition:var(--transition); }
        .input-field::placeholder { color:var(--text-muted); opacity:.7; }
        .input-field:focus { outline:none; border-color:var(--primary-accent); box-shadow:var(--focus-ring); }

        .checkbox-card { display:flex; align-items:center; padding:0.55rem 0.75rem; border:1px solid var(--border-color); border-radius:var(--radius-md); gap:0.55rem; background:var(--bg-soft); transition:var(--transition); }
        .checkbox-card:hover { background:var(--primary-soft); }

        .badge-risk { font-weight:600; font-size:.75rem; padding:.25rem .55rem; border-radius:var(--radius-sm); background:var(--primary-soft); color:var(--primary); }

        .card { background:var(--bg-panel); border:1px solid var(--border-color); border-radius:var(--radius-lg); padding:1.1rem 1.25rem; box-shadow:var(--shadow-sm); transition:var(--transition); }
        .card:hover { box-shadow:var(--shadow-md); }

    /* Utilidades personalizadas para que las clases existentes (text-primary, bg-primary...) funcionen */
    .text-primary { color: var(--primary) !important; }
    .text-primary-accent { color: var(--primary-accent) !important; }
    .bg-primary { background: var(--primary) !important; color:#fff !important; }
    .bg-primary-accent { background: var(--primary-accent) !important; color:#fff !important; }
    .bg-primary-soft { background: var(--primary-soft) !important; }
    .border-primary { border-color: var(--primary) !important; }
    .hover\:bg-primary:hover { background: var(--primary) !important; }
    .hover\:bg-primary-accent:hover { background: var(--primary-accent) !important; }
    .focus-ring { box-shadow: var(--focus-ring) !important; }

        .btn-soft { background:var(--primary-soft); color:var(--primary); border:1px solid var(--primary-soft); font-weight:600; }
        .btn-soft:hover { background:var(--primary-accent); color:#fff; }

        .fixed-action-bar { background:rgba(255,255,255,.92); backdrop-filter:blur(8px); box-shadow:0 4px 16px -4px rgba(0,0,0,0.18); }
        .dark-mode .fixed-action-bar { background:rgba(24,33,43,.9); }

        .high-contrast .input-field:focus { box-shadow:0 0 0 3px #0033dd55; }
        .dark-mode .checkbox-card { background:var(--bg-panel-alt); }
        .dark-mode .checkbox-card:hover { background:var(--primary-soft); }

        ::-webkit-scrollbar { width:10px; }
        ::-webkit-scrollbar-track { background:var(--bg-panel-alt); }
        ::-webkit-scrollbar-thumb { background:var(--border-color); border-radius:20px; border:2px solid var(--bg-panel-alt); }
        .dark-mode ::-webkit-scrollbar-thumb { background:#324556; border-color:#1f2a35; }

        .fade-in { animation:fade .4s ease; }
        @keyframes fade { from { opacity:0; transform:translateY(4px);} to {opacity:1; transform:translateY(0);} }
        </style>
        """
    )
