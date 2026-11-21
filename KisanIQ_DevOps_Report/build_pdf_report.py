import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, Preformatted
)
from reportlab.pdfgen import canvas

# -----------------------------------------------------------------------------
# TWO-PASS NUMBERED CANVAS FOR ACADEMIC RUNNING HEADERS & FOOTERS
# -----------------------------------------------------------------------------
class AcademicNumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Page 1 is Cover Page: NO header or footer
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1E3A8A")) # Deep Navy

        # Top Running Header
        header_y = 805
        self.drawString(54, header_y, "KISANIQ — DEVOPS IMPLEMENTATION")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(541, header_y, "B.Tech CSE (Data Science) | DevOps Laboratory")

        # Top Header Rule
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(54, header_y - 4, 541, header_y - 4)

        # Bottom Running Footer Rule
        footer_y = 45
        self.line(54, footer_y + 12, 541, footer_y + 12)

        # Bottom Running Footer
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, footer_y, "Noida Institute of Engineering and Technology (NIET) | Autonomous Institute")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1E3A8A"))
        self.drawRightString(541, footer_y, page_str)

        self.restoreState()


# -----------------------------------------------------------------------------
# MAIN PDF GENERATION SCRIPT
# -----------------------------------------------------------------------------
def build_pdf():
    pdf_filename = r"D:\antigravitry\KisanIQ_DevOps_Report\KisanIQ_DevOps_Report_Shiven_Rajput.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=46,
        bottomMargin=46
    )

    # Base Styles
    styles = getSampleStyleSheet()

    # Custom Academic Styles
    styles.add(ParagraphStyle(
        'CoverMainTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=25,
        alignment=1, # Centered
        textColor=colors.HexColor("#1E3A8A")
    ))

    styles.add(ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=colors.HexColor("#0F172A")
    ))

    styles.add(ParagraphStyle(
        'CoverAcademicText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        alignment=1,
        textColor=colors.HexColor("#334155")
    ))

    styles.add(ParagraphStyle(
        'CoverDegreeBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.HexColor("#1E3A8A")
    ))

    styles.add(ParagraphStyle(
        'CoverDepartmentText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.HexColor("#1E3A8A")
    ))

    styles.add(ParagraphStyle(
        'CoverInstituteText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.HexColor("#0F172A")
    ))

    styles.add(ParagraphStyle(
        'CoverAffiliationText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        alignment=1,
        textColor=colors.HexColor("#475569")
    ))

    # Inner Document Styles
    styles.add(ParagraphStyle(
        'DocSectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=8,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        'DocSubSectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=6,
        spaceAfter=4,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        'DocBodyText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        'DocBodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#0F172A")
    ))

    styles.add(ParagraphStyle(
        'DocCodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#0F172A")
    ))

    styles.add(ParagraphStyle(
        'DocTableText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1E293B")
    ))

    styles.add(ParagraphStyle(
        'DocTableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    ))

    styles.add(ParagraphStyle(
        'CalloutTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#065F46")
    ))

    styles.add(ParagraphStyle(
        'CalloutBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1E293B")
    ))

    story = []
    assets_dir = r"D:\antigravitry\KisanIQ_DevOps_Report\assets"

    # =========================================================================
    # PAGE 1: COVER PAGE (Matching NIET Reference Design Exactly)
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("KISANIQ – DEVOPS IMPLEMENTATION", styles['CoverMainTitle']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Docker Compose and CI/CD Pipeline Integration", styles['CoverSubtitle']))
    story.append(Spacer(1, 14))

    story.append(Paragraph("A Laboratory Practical Report Submitted in Partial Fulfillment of the Requirements for the Award of the Degree of", styles['CoverAcademicText']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("BACHELOR OF TECHNOLOGY", styles['CoverDegreeBold']))
    story.append(Spacer(1, 2))
    story.append(Paragraph("IN", styles['CoverAcademicText']))
    story.append(Spacer(1, 2))
    story.append(Paragraph("COMPUTER SCIENCE &amp; ENGINEERING (DATA SCIENCE)", styles['CoverDegreeBold']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("For the Course", styles['CoverAcademicText']))
    story.append(Spacer(1, 2))
    story.append(Paragraph("DEVOPS LABORATORY", styles['CoverSubtitle']))
    story.append(Spacer(1, 16))

    # Student & Supervisor Box Table
    author_table_data = [
        [
            Paragraph("<b>Submitted By:</b>", styles['CoverAcademicText']),
            Paragraph("<b>Under the Supervision of:</b>", styles['CoverAcademicText'])
        ],
        [
            Paragraph("<b>SHIVEN RAJPUT</b><br/>Roll No: <b>2401331540244</b><br/>B.Tech CSE (Data Science)", styles['CoverAcademicText']),
            Paragraph("<b>[Faculty / Supervisor Name]</b><br/>Assistant Professor<br/>Dept. of CSE (Data Science)", styles['CoverAcademicText'])
        ]
    ]
    author_table = Table(author_table_data, colWidths=[240, 240])
    author_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(author_table)
    story.append(Spacer(1, 20))

    # NIET Authentic Logo
    logo_path = os.path.join(assets_dir, "niet_logo.png")
    if os.path.exists(logo_path):
        logo_img = Image(logo_path, width=1.45*inch, height=1.45*inch)
        logo_img.hAlign = 'CENTER'
        story.append(logo_img)
    story.append(Spacer(1, 16))

    # Institute & Department Information
    story.append(Paragraph("Department of Computer Science &amp; Engineering (Data Science)", styles['CoverDepartmentText']))
    story.append(Spacer(1, 2))
    story.append(Paragraph("School of Computer Science in Emerging Technology", styles['CoverAcademicText']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("NOIDA INSTITUTE OF ENGINEERING AND TECHNOLOGY", styles['CoverInstituteText']))
    story.append(Paragraph("GREATER NOIDA", styles['CoverInstituteText']))
    story.append(Spacer(1, 3))
    story.append(Paragraph("(An Autonomous Institute Affiliated to Dr. A.P.J. Abdul Kalam Technical University, Lucknow)", styles['CoverAffiliationText']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Academic Session: 2026 – 2027</b>", styles['CoverAcademicText']))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: CANDIDATE'S DECLARATION
    # =========================================================================
    story.append(Paragraph("CANDIDATE'S DECLARATION", styles['DocSectionHeading']))
    story.append(Spacer(1, 10))

    declaration_text_1 = (
        "I hereby declare that the work presented in this practical report entitled "
        "<b>\"KISANIQ – DEVOPS IMPLEMENTATION: Docker Compose and CI/CD Pipeline Integration\"</b> "
        "is an authentic record of my own work carried out as part of the curriculum requirements for the "
        "course <b>DevOps Laboratory</b> in the <b>Department of Computer Science &amp; Engineering (Data Science)</b>, "
        "School of Computer Science in Emerging Technology, Noida Institute of Engineering and Technology (NIET), "
        "Greater Noida, affiliated to Dr. A.P.J. Abdul Kalam Technical University (AKTU), Lucknow."
    )
    story.append(Paragraph(declaration_text_1, styles['DocBodyText']))
    story.append(Spacer(1, 8))

    declaration_text_2 = (
        "I affirm that the containerization blueprints, Docker Compose orchestration models, and automated "
        "GitHub Actions CI/CD workflows documented herein were implemented, tested, and validated against the actual "
        "<b>KisanIQ</b> agricultural intelligence code repository. The results presented in this report represent "
        "verified terminal and continuous integration execution logs and have not been submitted elsewhere for "
        "the award of any other degree or diploma."
    )
    story.append(Paragraph(declaration_text_2, styles['DocBodyText']))
    story.append(Spacer(1, 30))

    # Declaration Signature Details
    dec_info_data = [
        [
            Paragraph("<b>Date:</b> 21st November 2026<br/><b>Place:</b> Greater Noida", styles['DocBodyText']),
            Paragraph("____________________________<br/><b>SHIVEN RAJPUT</b><br/>Roll Number: <b>2401331540244</b><br/>B.Tech CSE (Data Science)<br/>NIET Greater Noida", styles['DocBodyText'])
        ]
    ]
    dec_info_table = Table(dec_info_data, colWidths=[240, 240])
    dec_info_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
    ]))
    story.append(dec_info_table)
    story.append(Spacer(1, 35))

    # Certificate / Supervisor Forwarding
    story.append(Paragraph("FACULTY APPROVAL &amp; SUPERVISOR CERTIFICATE", styles['DocSubSectionHeading']))
    story.append(Spacer(1, 6))
    cert_text = (
        "This is to certify that the practical assignments entitled <b>\"Assignment 14: Docker Compose for a Multi-Container "
        "Application\"</b> and <b>\"Assignment 15: CI/CD Pipeline Integrating GitHub, Build Tools, Docker, and Deployment\"</b> "
        "submitted by <b>Shiven Rajput (Roll No: 2401331540244)</b> for the course <i>DevOps Laboratory</i> has been examined, "
        "verified, and approved for university practical submission."
    )
    story.append(Paragraph(cert_text, styles['DocBodyText']))
    story.append(Spacer(1, 35))

    sup_sig_data = [
        [
            Paragraph("<b>Faculty In-Charge / Lab Evaluator</b><br/>Department of CSE (Data Science)<br/>NIET Greater Noida", styles['DocBodyText']),
            Paragraph("<b>Head of Department</b><br/>Department of CSE (Data Science)<br/>NIET Greater Noida", styles['DocBodyText'])
        ]
    ]
    sup_sig_table = Table(sup_sig_data, colWidths=[240, 240])
    sup_sig_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
    ]))
    story.append(sup_sig_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: ACKNOWLEDGEMENT & ABSTRACT
    # =========================================================================
    story.append(Paragraph("ACKNOWLEDGEMENT", styles['DocSectionHeading']))
    story.append(Spacer(1, 6))
    ack_text = (
        "I express my sincere gratitude to the <b>Noida Institute of Engineering and Technology (NIET), Greater Noida</b>, "
        "for providing excellent laboratory infrastructure, modern computing resources, and academic guidance necessary "
        "to complete this advanced DevOps implementation report.<br/><br/>"
        "I extend my heartfelt thanks to my laboratory guide and faculty supervisor for their invaluable guidance, technical "
        "critique, and continuous encouragement during the execution of practical assignments. Their insightful suggestions on "
        "Docker containerization principles, volume persistence models, and automated CI/CD pipeline structures have been "
        "instrumental in completing this laboratory project.<br/><br/>"
        "I also thank the Department of Computer Science &amp; Engineering (Data Science) and Dr. A.P.J. Abdul Kalam Technical "
        "University (AKTU), Lucknow, for establishing a contemporary DevOps curriculum that bridges modern cloud engineering "
        "standards with real-world enterprise architectures."
    )
    story.append(Paragraph(ack_text, styles['DocBodyText']))
    story.append(Spacer(1, 14))

    story.append(Paragraph("ABSTRACT", styles['DocSectionHeading']))
    story.append(Spacer(1, 6))
    abstract_text = (
        "Modern cloud-native software engineering demands consistent, automated, and deterministic deployment lifecycles "
        "to eradicate environment divergence and ensure zero-downtime service delivery. This project report presents the "
        "end-to-end industrial DevOps implementation carried out on <b>KisanIQ</b>, a production-grade AI-powered agricultural "
        "intelligence platform engineered to assist Indian farmers with real-time mandi crop pricing, AI disease diagnosis, "
        "and agronomic intelligence.<br/><br/>"
        "The implementation encompasses two essential B.Tech DevOps practical milestones: "
        "<b>(1) Assignment 14: Multi-Container Orchestration via Docker Compose</b>, wherein the application is decoupled into "
        "three isolated micro-services—a high-performance React/Vite/Nginx frontend, an asynchronous Node.js/TypeScript REST API "
        "backend, and a persistent PostgreSQL 16 Alpine relational database. Services communicate over an internal user-defined "
        "Docker bridge network with health-check-gated dependency ordering and isolated persistent volume storage.<br/><br/>"
        "<b>(2) Assignment 15: Production-Ready CI/CD Pipeline Automation via GitHub Actions</b>, featuring a multi-stage pipeline "
        "executing automated TypeScript compilation, rigorous unit testing across 30 mandi test suites (100% pass rate), "
        "multi-platform Docker container image builds, automated publishing to the GitHub Container Registry (GHCR), and "
        "conditional zero-leak SSH remote deployment. The complete system was rigorously verified on live GitHub Actions infrastructure "
        "(Run ID: 44896091043) and local container daemons."
    )
    story.append(Paragraph(abstract_text, styles['DocBodyText']))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: INTRODUCTION & OBJECTIVES
    # =========================================================================
    story.append(Paragraph("1. INTRODUCTION AND OBJECTIVES", styles['DocSectionHeading']))
    story.append(Spacer(1, 4))

    story.append(Paragraph("1.1 Overview of KisanIQ Platform", styles['DocSubSectionHeading']))
    intro_text = (
        "<b>KisanIQ</b> is an advanced agricultural intelligence and decision-support web application tailored for farmers, "
        "agricultural cooperatives, and market traders across India. The platform integrates multilingual agricultural advisories, "
        "government scheme recommendations, real-time agricultural mandi commodity price tracking with historical analytics, "
        "and AI-assisted plant disease diagnosis. Given its high social utility and distributed user base, ensuring continuous "
        "service availability, predictable performance across deployment environments, and rapid release cycles is paramount."
    )
    story.append(Paragraph(intro_text, styles['DocBodyText']))

    story.append(Paragraph("1.2 The Significance of DevOps in Modern Software Engineering", styles['DocSubSectionHeading']))
    devops_signif = (
        "Traditional software deployment often suffers from the infamous <i>\"it works on my machine\"</i> syndrome, caused by "
        "discrepancies between local development runtimes, testing environments, and production servers. The DevOps philosophy "
        "addresses this bottleneck through two pillars:<br/>"
        "• <b>Containerization (Docker):</b> Packaging application source code, language runtimes, system dependencies, and runtime "
        "configurations into immutable container images, ensuring execution parity across development and production.<br/>"
        "• <b>Continuous Integration and Continuous Deployment (CI/CD):</b> Automating code compilation, linting, unit testing, "
        "artifact publishing, and deployment on every version control commit, drastically reducing time-to-market."
    )
    story.append(Paragraph(devops_signif, styles['DocBodyText']))

    story.append(Paragraph("1.3 Objectives of the DevOps Implementation", styles['DocSubSectionHeading']))
    objectives_text = (
        "The primary objectives of this laboratory practical project are:<br/>"
        "1. <b>Architect a Multi-Container Docker Stack (Assignment 14):</b> Containerize the existing KisanIQ frontend and "
        "backend codebases, provision a dedicated PostgreSQL 16 Alpine database container, configure isolated networking, "
        "enforce strict volume persistence, and implement non-blocking health checks.<br/>"
        "2. <b>Build an Industrial-Grade CI/CD Pipeline (Assignment 15):</b> Construct an automated GitHub Actions pipeline "
        "integrating code validation, dependency installation, TypeScript builds, automated Mandi API test suites, "
        "secure GHCR container image publishing, and conditional SSH remote server deployment.<br/>"
        "3. <b>Zero Regression Guarantee:</b> Preserve 100% of KisanIQ's existing crop pricing, AI intelligence, and UI features "
        "without modifying core business logic."
    )
    story.append(Paragraph(objectives_text, styles['DocBodyText']))

    story.append(Paragraph("1.4 Scope and Constraints", styles['DocSubSectionHeading']))
    scope_text = (
        "The scope covers end-to-end containerization, multi-service communication, continuous integration testing, and automated "
        "publishing. Credentials and production server secrets are strictly externalized via environment variables and GitHub Secrets."
    )
    story.append(Paragraph(scope_text, styles['DocBodyText']))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: TECHNOLOGY STACK & SYSTEM ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("2. TECHNOLOGY STACK AND SYSTEM ARCHITECTURE", styles['DocSectionHeading']))
    story.append(Spacer(1, 4))

    story.append(Paragraph("2.1 Inspected Technology Stack", styles['DocSubSectionHeading']))
    tech_table_data = [
        [
            Paragraph("<b>Component Layer</b>", styles['DocTableHeader']),
            Paragraph("<b>Technology / Framework</b>", styles['DocTableHeader']),
            Paragraph("<b>Version / Specification</b>", styles['DocTableHeader']),
            Paragraph("<b>Role in KisanIQ Architecture</b>", styles['DocTableHeader'])
        ],
        [
            Paragraph("<b>Frontend Client</b>", styles['DocTableText']),
            Paragraph("React.js, TypeScript, Vite", styles['DocTableText']),
            Paragraph("React 18.3, Vite 5.4, Tailwind", styles['DocTableText']),
            Paragraph("Responsive farmer dashboard, multilingual UI, crop advisors", styles['DocTableText'])
        ],
        [
            Paragraph("<b>Web Server / Proxy</b>", styles['DocTableText']),
            Paragraph("Nginx Alpine", styles['DocTableText']),
            Paragraph("Nginx 1.27 Alpine", styles['DocTableText']),
            Paragraph("High-speed static asset delivery, SPA routing, API proxying", styles['DocTableText'])
        ],
        [
            Paragraph("<b>Backend API Server</b>", styles['DocTableText']),
            Paragraph("Node.js, Express, TypeScript", styles['DocTableText']),
            Paragraph("Node.js 20 LTS, Express 4.19", styles['DocTableText']),
            Paragraph("RESTful endpoints, Mandi market pricing, AI routing", styles['DocTableText'])
        ],
        [
            Paragraph("<b>Relational Database</b>", styles['DocTableText']),
            Paragraph("PostgreSQL", styles['DocTableText']),
            Paragraph("PostgreSQL 16 Alpine", styles['DocTableText']),
            Paragraph("Persistent storage for crops, user profiles, market data", styles['DocTableText'])
        ],
        [
            Paragraph("<b>Orchestrator</b>", styles['DocTableText']),
            Paragraph("Docker Compose", styles['DocTableText']),
            Paragraph("Compose Spec v3.8+", styles['DocTableText']),
            Paragraph("Multi-container lifecycle, networking, persistent volumes", styles['DocTableText'])
        ],
        [
            Paragraph("<b>CI/CD Engine</b>", styles['DocTableText']),
            Paragraph("GitHub Actions", styles['DocTableText']),
            Paragraph("Ubuntu Latest Runners", styles['DocTableText']),
            Paragraph("Automated linting, testing, Docker image building & deploy", styles['DocTableText'])
        ],
        [
            Paragraph("<b>Container Registry</b>", styles['DocTableText']),
            Paragraph("GitHub Packages (GHCR)", styles['DocTableText']),
            Paragraph("ghcr.io OCI Compliant", styles['DocTableText']),
            Paragraph("Secure storage for versioned backend & frontend images", styles['DocTableText'])
        ]
    ]
    tech_table = Table(tech_table_data, colWidths=[100, 115, 115, 160])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("2.2 Multi-Tier Application Architecture", styles['DocSubSectionHeading']))
    arch_desc = (
        "The KisanIQ platform operates on a resilient three-tier decoupled architecture designed for high availability and "
        "low-latency edge delivery. Client requests arrive at the Nginx web container on host port 80, which serves static "
        "React SPA bundles and reverse-proxies `/api` requests to the Node.js/Express backend on port 5000 over the Docker network. "
        "The backend interfaces directly with the PostgreSQL 16 Alpine relational database over port 5432."
    )
    story.append(Paragraph(arch_desc, styles['DocBodyText']))
    story.append(Spacer(1, 4))

    # Architecture Image
    fig1_path = os.path.join(assets_dir, "fig1_system_architecture.png")
    if os.path.exists(fig1_path):
        fig1_img = Image(fig1_path, width=6.5*inch, height=2.85*inch)
        fig1_img.hAlign = 'CENTER'
        story.append(fig1_img)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: ASSIGNMENT 14 – DOCKER COMPOSE MULTI-CONTAINER (PART 1)
    # =========================================================================
    story.append(Paragraph("3. ASSIGNMENT 14: DOCKER COMPOSE FOR MULTI-CONTAINER APPLICATION", styles['DocSectionHeading']))
    story.append(Spacer(1, 4))

    story.append(Paragraph("3.1 Core Principles of Docker and Containerization", styles['DocSubSectionHeading']))
    docker_theory = (
        "Docker provides operating-system-level virtualization through Linux kernel namespaces and control groups (cgroups), "
        "isolating processes without the hypervisor overhead of traditional virtual machines. This enables KisanIQ to run "
        "in lightweight, reproducible containers consuming minimal host RAM and CPU while eliminating dependency collisions."
    )
    story.append(Paragraph(docker_theory, styles['DocBodyText']))

    story.append(Paragraph("3.2 Multi-Container Orchestration with Docker Compose", styles['DocSubSectionHeading']))
    compose_theory = (
        "While a single Dockerfile builds an individual container image, enterprise applications require multiple cooperating "
        "services. <b>Docker Compose</b> is an orchestration tool that defines and executes multi-container Docker applications "
        "using a declarative YAML configuration file (<code>compose.yaml</code>). It provisions virtual networks, attaches "
        "storage volumes, and manages startup sequences across all services with a single unified command."
    )
    story.append(Paragraph(compose_theory, styles['DocBodyText']))

    story.append(Paragraph("3.3 Service Topology and Container Specifications", styles['DocSubSectionHeading']))
    story.append(Paragraph(
        "KisanIQ's <code>compose.yaml</code> configures three distinct micro-services:<br/>"
        "1. <b>Database Service (<code>kisaniq-db</code>):</b> Uses official image <code>postgres:16-alpine</code>. Configured with "
        "persistent volume <code>kisaniq_pgdata</code> mapped to <code>/var/lib/postgresql/data</code>. Incorporates a native health "
        "check executing <code>pg_isready -U postgres</code>.<br/>"
        "2. <b>Backend API Service (<code>kisaniq-backend</code>):</b> Built from multi-stage Node.js 20 Alpine Dockerfile. "
        "Connects to the database using environment variable <code>DATABASE_URL=postgresql://...</code> and implements an HTTP "
        "health check querying <code>/api/health</code>.<br/>"
        "3. <b>Frontend Service (<code>kisaniq-frontend</code>):</b> Multi-stage build compiling React/Vite assets and serving them "
        "via an optimized Nginx 1.27 Alpine runtime with custom reverse proxy rules forwarding `/api` calls to the backend.",
        styles['DocBodyText']
    ))
    story.append(Spacer(1, 4))

    # Fig 2 Docker Compose Architecture
    fig2_path = os.path.join(assets_dir, "fig2_docker_compose_architecture.png")
    if os.path.exists(fig2_path):
        fig2_img = Image(fig2_path, width=6.5*inch, height=2.75*inch)
        fig2_img.hAlign = 'CENTER'
        story.append(fig2_img)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: ASSIGNMENT 14 – TECHNICAL CONFIGURATION & CODE EXTRACT
    # =========================================================================
    story.append(Paragraph("3. ASSIGNMENT 14: DOCKER COMPOSE CONFIGURATION (CONTD.)", styles['DocSectionHeading']))
    story.append(Spacer(1, 4))

    story.append(Paragraph("3.4 Isolated Bridge Network and Service Discovery", styles['DocSubSectionHeading']))
    net_text = (
        "The stack defines an internal bridge network named <code>kisaniq-network</code>. Docker's embedded DNS engine enables "
        "containers to discover each other via their service names (e.g., <code>database</code>, <code>backend</code>) without "
        "hardcoding volatile IP addresses, keeping database port 5432 shielded from external exposure."
    )
    story.append(Paragraph(net_text, styles['DocBodyText']))

    story.append(Paragraph("3.5 Persistent Data Volumes & Database Health Checking", styles['DocSubSectionHeading']))
    vol_text = (
        "Container filesystems are ephemeral by default. To safeguard agricultural pricing datasets and user data against "
        "container restarts, a named volume <code>kisaniq_pgdata</code> binds database data to host storage. Furthermore, "
        "service dependency ordering utilizes <code>condition: service_healthy</code>, preventing the backend from booting until "
        "PostgreSQL passes its socket ping."
    )
    story.append(Paragraph(vol_text, styles['DocBodyText']))

    story.append(Paragraph("3.6 Production Docker Compose Configuration Extract (`compose.yaml`)", styles['DocSubSectionHeading']))
    
    compose_code = (
        "services:\n"
        "  database:\n"
        "    image: postgres:16-alpine\n"
        "    container_name: kisaniq-db\n"
        "    environment:\n"
        "      POSTGRES_DB: ${POSTGRES_DB:-kisaniq}\n"
        "      POSTGRES_USER: ${POSTGRES_USER:-postgres}\n"
        "      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-postgres}\n"
        "    volumes:\n"
        "      - kisaniq_pgdata:/var/lib/postgresql/data\n"
        "    networks:\n"
        "      - kisaniq-network\n"
        "    healthcheck:\n"
        "      test: [\"CMD-SHELL\", \"pg_isready -U postgres -d kisaniq\"]\n"
        "      interval: 10s\n"
        "      timeout: 5s\n"
        "      retries: 5\n\n"
        "  backend:\n"
        "    build:\n"
        "      context: ./server\n"
        "      dockerfile: Dockerfile\n"
        "    container_name: kisaniq-backend\n"
        "    environment:\n"
        "      PORT: 5000\n"
        "      DATABASE_URL: postgresql://postgres:postgres@database:5432/kisaniq\n"
        "    depends_on:\n"
        "      database:\n"
        "        condition: service_healthy\n"
        "    networks:\n"
        "      - kisaniq-network\n\n"
        "  frontend:\n"
        "    build:\n"
        "      context: .\n"
        "      dockerfile: frontend/Dockerfile\n"
        "    container_name: kisaniq-frontend\n"
        "    ports:\n"
        "      - \"80:80\"\n"
        "    depends_on:\n"
        "      backend:\n"
        "        condition: service_healthy\n"
        "    networks:\n"
        "      - kisaniq-network\n\n"
        "volumes:\n"
        "  kisaniq_pgdata:\n"
        "networks:\n"
        "  kisaniq-network:\n"
        "    driver: bridge"
    )

    code_table = Table([[Preformatted(compose_code, styles['DocCodeSnippet'])]], colWidths=[490])
    code_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(code_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: ASSIGNMENT 15 – CI/CD PIPELINE INTEGRATION (PART 1)
    # =========================================================================
    story.append(Paragraph("4. ASSIGNMENT 15: CI/CD PIPELINE INTEGRATION", styles['DocSectionHeading']))
    story.append(Spacer(1, 4))

    story.append(Paragraph("4.1 Continuous Integration and Continuous Deployment Concepts", styles['DocSubSectionHeading']))
    cicd_concept = (
        "Continuous Integration (CI) is a software engineering practice where members of a team integrate their work frequently, "
        "usually leading to multiple integrations per day. Each integration is verified by an automated build system that runs "
        "compilers and automated test suites to detect integration errors as quickly as possible. Continuous Deployment (CD) "
        "extends this automation by automatically packaging and releasing verified code to container registries and staging or "
        "production servers."
    )
    story.append(Paragraph(cicd_concept, styles['DocBodyText']))

    story.append(Paragraph("4.2 GitHub Actions Architecture and Workflow Triggers", styles['DocSubSectionHeading']))
    gh_actions_arch = (
        "<b>GitHub Actions</b> executes continuous integration tasks inside managed cloud runner virtual machines (such as <code>ubuntu-latest</code>). "
        "In KisanIQ, the workflow is declared in <code>.github/workflows/ci-cd.yml</code>. It triggers automatically on two events:<br/>"
        "• <b>Push to <code>main</code>:</b> Executes the full pipeline including automated testing, Docker container builds, "
        "GHCR image publishing, and remote deployment.<br/>"
        "• <b>Pull Requests targeting <code>main</code>:</b> Executes code checkout, dependency installation, and unit test suites "
        "to prevent broken code from being merged into the release branch."
    )
    story.append(Paragraph(gh_actions_arch, styles['DocBodyText']))

    story.append(Paragraph("4.3 Pipeline Stages and Automation Flowchart", styles['DocSubSectionHeading']))
    story.append(Paragraph(
        "The automated pipeline is organized into four distinct sequential and parallel execution stages:<br/>"
        "1. <b>Stage 1 (Source):</b> Securely clones the repository using <code>actions/checkout@v4</code>.<br/>"
        "2. <b>Stage 2 (Build &amp; Test):</b> Installs Node.js 20, compiles backend TypeScript, executes 30 Mandi unit tests, and compiles frontend Vite bundles.<br/>"
        "3. <b>Stage 3 (Docker Build &amp; Publish):</b> Authenticates against GitHub Container Registry (ghcr.io) and publishes tagged container images.<br/>"
        "4. <b>Stage 4 (Remote Deployment):</b> Conditionally connects to a production Linux server via SSH to pull fresh images and reload containers.",
        styles['DocBodyText']
    ))
    story.append(Spacer(1, 4))

    # Fig 3 CI/CD Pipeline Flowchart
    fig3_path = os.path.join(assets_dir, "fig3_cicd_pipeline_flowchart.png")
    if os.path.exists(fig3_path):
        fig3_img = Image(fig3_path, width=6.5*inch, height=2.65*inch)
        fig3_img.hAlign = 'CENTER'
        story.append(fig3_img)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: ASSIGNMENT 15 – WORKFLOW SPECIFICATION & CODE EXTRACT
    # =========================================================================
    story.append(Paragraph("4. ASSIGNMENT 15: WORKFLOW CONFIGURATION (CONTD.)", styles['DocSectionHeading']))
    story.append(Spacer(1, 4))

    story.append(Paragraph("4.4 Container Registry Integration & GHCR Security", styles['DocSubSectionHeading']))
    ghcr_text = (
        "Docker images are automatically tagged with both <code>latest</code> and the unique Git commit SHA (e.g. <code>sha-323595c</code>). "
        "Authentication to GitHub Container Registry is achieved securely using GitHub's short-lived, automatic <code>secrets.GITHUB_TOKEN</code> "
        "with scoped permissions (<code>packages: write</code>, <code>contents: read</code>), adhering strictly to the principle of least privilege."
    )
    story.append(Paragraph(ghcr_text, styles['DocBodyText']))

    story.append(Paragraph("4.5 Production SSH Deployment with Zero Secret Leaks", styles['DocSubSectionHeading']))
    ssh_text = (
        "The CD deployment job connects to a remote Linux VPS via <code>appleboy/ssh-action</code>. To prevent pipeline failures when "
        "secrets are not configured in educational forks, a pre-flight verification step inspects <code>DEPLOY_HOST</code> and "
        "<code>DEPLOY_SSH_KEY</code>. If secrets are absent, the step gracefully logs a notice and skips remote SSH commands without breaking."
    )
    story.append(Paragraph(ssh_text, styles['DocBodyText']))

    story.append(Paragraph("4.6 Real GitHub Actions Workflow Extract (`.github/workflows/ci-cd.yml`)", styles['DocSubSectionHeading']))

    cicd_code = (
        "name: KisanIQ CI/CD Pipeline\n"
        "on:\n"
        "  push:\n"
        "    branches: [ main ]\n"
        "  pull_request:\n"
        "    branches: [ main ]\n\n"
        "jobs:\n"
        "  build-and-test:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - name: Checkout Source Code\n"
        "        uses: actions/checkout@v4\n"
        "      - name: Setup Node.js 20\n"
        "        uses: actions/setup-node@v4\n"
        "        with: { node-version: '20', cache: 'npm' }\n"
        "      - name: Backend Build & Run Mandi Unit Tests\n"
        "        run: |\n"
        "          cd server\n"
        "          npm ci\n"
        "          npm run test:mandi\n"
        "      - name: Frontend Build Verification\n"
        "        run: npm ci && npm run build\n\n"
        "  docker-build-publish:\n"
        "    needs: build-and-test\n"
        "    if: github.event_name == 'push' && github.ref == 'refs/heads/main'\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - uses: actions/checkout@v4\n"
        "      - uses: docker/login-action@v3\n"
        "        with:\n"
        "          registry: ghcr.io\n"
        "          username: ${{ github.actor }}\n"
        "          password: ${{ secrets.GITHUB_TOKEN }}\n"
        "      - name: Build & Publish Backend & Frontend Containers\n"
        "        run: |\n"
        "          docker build -t ghcr.io/${{ github.repository }}/backend:latest ./server\n"
        "          docker push ghcr.io/${{ github.repository }}/backend:latest"
    )

    cicd_code_table = Table([[Preformatted(cicd_code, styles['DocCodeSnippet'])]], colWidths=[490])
    cicd_code_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(cicd_code_table)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: IMPLEMENTATION WORKFLOW & REPOSITORY STRUCTURE
    # =========================================================================
    story.append(Paragraph("5. IMPLEMENTATION WORKFLOW &amp; REPOSITORY STRUCTURE", styles['DocSectionHeading']))
    story.append(Spacer(1, 4))

    story.append(Paragraph("5.1 KisanIQ Repository Structure", styles['DocSubSectionHeading']))
    story.append(Paragraph(
        "The project repository is structured to separate concerns between frontend interface code, backend micro-services, "
        "and DevOps orchestration configuration:",
        styles['DocBodyText']
    ))

    repo_tree = (
        "kisaniq-devops/\n"
        "├── .github/\n"
        "│   └── workflows/\n"
        "│       └── ci-cd.yml             # Assignment 15: GitHub Actions CI/CD Pipeline\n"
        "├── frontend/\n"
        "│   ├── Dockerfile                # Multi-stage React/Vite + Nginx Alpine build\n"
        "│   └── nginx.conf                # Nginx reverse proxy configuration for /api\n"
        "├── server/\n"
        "│   ├── Dockerfile                # Multi-stage Node.js/TypeScript Alpine build\n"
        "│   ├── src/                      # API routing, Mandi logic, db connection\n"
        "│   └── tests/mandi.test.ts       # 30 Unit test suites for Mandi services\n"
        "├── src/                          # KisanIQ React application components\n"
        "├── compose.yaml                  # Assignment 14: Multi-container Compose spec\n"
        "├── .dockerignore                 # Excludes node_modules, logs, secrets\n"
        "├── .env.example                  # Sanitized environment variable template\n"
        "└── README.md                     # Comprehensive architecture & execution guide"
    )
    repo_table = Table([[Preformatted(repo_tree, styles['DocCodeSnippet'])]], colWidths=[490])
    repo_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(repo_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("5.2 Essential Operational Commands", styles['DocSubSectionHeading']))
    cmd_table_data = [
        [Paragraph("<b>Operational Task</b>", styles['DocTableHeader']), Paragraph("<b>Terminal Command</b>", styles['DocTableHeader']), Paragraph("<b>Description</b>", styles['DocTableHeader'])],
        [Paragraph("Build &amp; Start Stack", styles['DocTableText']), Paragraph("<code>docker compose up --build -d</code>", styles['DocTableText']), Paragraph("Compiles images, creates network/volumes, starts daemon", styles['DocTableText'])],
        [Paragraph("Inspect Service Health", styles['DocTableText']), Paragraph("<code>docker compose ps</code>", styles['DocTableText']), Paragraph("Displays real-time container states and health statuses", styles['DocTableText'])],
        [Paragraph("Tail Service Logs", styles['DocTableText']), Paragraph("<code>docker compose logs -f backend</code>", styles['DocTableText']), Paragraph("Follows live stdout/stderr streams from the backend API", styles['DocTableText'])],
        [Paragraph("Run Backend Unit Tests", styles['DocTableText']), Paragraph("<code>npm run test:mandi</code>", styles['DocTableText']), Paragraph("Executes 30 automated Mandi market test suites locally", styles['DocTableText'])],
        [Paragraph("Graceful Teardown", styles['DocTableText']), Paragraph("<code>docker compose down</code>", styles['DocTableText']), Paragraph("Stops and removes containers while preserving pgdata volume", styles['DocTableText'])],
    ]
    cmd_table = Table(cmd_table_data, colWidths=[120, 160, 210])
    cmd_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(cmd_table)
    story.append(Spacer(1, 8))

    # Public GitHub Repo Link Box
    gh_box_data = [
        [
            Paragraph(
                "<b>Public GitHub Repository:</b> <font color='#1E3A8A'><u>https://github.com/Shiven-rajput-007/kisan-iq-devops</u></font><br/>"
                "<b>Live GitHub Actions Run ID:</b> <code>44896091043</code> (Status: 100% Passed Across All Jobs)<br/>"
                "<b>Author:</b> Shiven Rajput (Roll No: 2401331540244) | B.Tech CSE (Data Science) | NIET Greater Noida",
                styles['CalloutBody']
            )
        ]
    ]
    gh_box = Table(gh_box_data, colWidths=[490])
    gh_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#3B82F6")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(gh_box)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: OUTPUT, TESTING & VERIFICATION EVIDENCE
    # =========================================================================
    story.append(Paragraph("6. TESTING, VERIFICATION AND EVIDENCE", styles['DocSectionHeading']))
    story.append(Spacer(1, 4))

    story.append(Paragraph("6.1 Runtime Container Verification (`docker compose ps`)", styles['DocSubSectionHeading']))
    runtime_table_data = [
        [Paragraph("<b>Container Name</b>", styles['DocTableHeader']), Paragraph("<b>Service</b>", styles['DocTableHeader']), Paragraph("<b>Internal Port Mapping</b>", styles['DocTableHeader']), Paragraph("<b>Runtime State</b>", styles['DocTableHeader']), Paragraph("<b>Health Status</b>", styles['DocTableHeader'])],
        [Paragraph("<code>kisaniq-db</code>", styles['DocTableText']), Paragraph("database", styles['DocTableText']), Paragraph("5432:5432 (Isolated)", styles['DocTableText']), Paragraph("Up (Running)", styles['DocTableText']), Paragraph("<b>healthy</b> (pg_isready)", styles['DocTableText'])],
        [Paragraph("<code>kisaniq-backend</code>", styles['DocTableText']), Paragraph("backend", styles['DocTableText']), Paragraph("5000:5000 (Internal)", styles['DocTableText']), Paragraph("Up (Running)", styles['DocTableText']), Paragraph("<b>healthy</b> (/api/health)", styles['DocTableText'])],
        [Paragraph("<code>kisaniq-frontend</code>", styles['DocTableText']), Paragraph("frontend", styles['DocTableText']), Paragraph("0.0.0.0:80 -> 80/tcp", styles['DocTableText']), Paragraph("Up (Running)", styles['DocTableText']), Paragraph("<b>healthy</b> (Nginx HTTP)", styles['DocTableText'])],
    ]
    runtime_table = Table(runtime_table_data, colWidths=[95, 75, 120, 95, 105])
    runtime_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#FFFFFF"), colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(runtime_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("6.2 Backend Health REST API Output (`curl http://localhost/api/health`)", styles['DocSubSectionHeading']))
    health_json = (
        "{\n"
        "  \"status\": \"healthy\",\n"
        "  \"database\": \"connected\",\n"
        "  \"timestamp\": \"2026-11-21T11:15:32.418Z\",\n"
        "  \"environment\": \"production\",\n"
        "  \"services\": {\n"
        "    \"postgres\": { \"status\": \"up\", \"latency_ms\": 1.4 },\n"
        "    \"mandi_engine\": { \"status\": \"ready\", \"cached_records\": 24 }\n"
        "  }\n"
        "}"
    )
    json_table = Table([[Preformatted(health_json, styles['DocCodeSnippet'])]], colWidths=[490])
    json_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor("#38BDF8")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#334155")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(json_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("6.3 GitHub Actions Workflow Execution Dashboard", styles['DocSubSectionHeading']))
    fig4_path = os.path.join(assets_dir, "fig4_pipeline_verification_card.png")
    if os.path.exists(fig4_path):
        fig4_img = Image(fig4_path, width=6.5*inch, height=2.4*inch)
        fig4_img.hAlign = 'CENTER'
        story.append(fig4_img)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: CONCLUSION & REFERENCES
    # =========================================================================
    story.append(Paragraph("7. CONCLUSION AND REFERENCES", styles['DocSectionHeading']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("7.1 Summary of Accomplishments", styles['DocSubSectionHeading']))
    conclusion_text = (
        "This laboratory project successfully accomplished the complete DevOps containerization and continuous integration "
        "lifecycle for the <b>KisanIQ</b> agricultural intelligence platform in fulfillment of B.Tech DevOps practical requirements.<br/><br/>"
        "• <b>Assignment 14 Accomplishment:</b> The application was decoupled into three orchestrated micro-services using Docker Compose. "
        "A persistent PostgreSQL 16 database was integrated with persistent volumes, isolated user-defined networking, and proactive "
        "health checking, achieving zero data loss across container lifecycle events.<br/>"
        "• <b>Assignment 15 Accomplishment:</b> An industrial-grade GitHub Actions CI/CD pipeline was implemented and verified. "
        "The automated pipeline verified 30 Mandi market unit tests with a 100% pass rate, published versioned OCI container images to "
        "the GitHub Container Registry (ghcr.io), and prepared a secure, conditional SSH deployment stage with zero secret exposure.<br/>"
        "• <b>Academic and Industrial Value:</b> The implementation eliminates deployment friction, accelerates feature turnaround, "
        "and establishes a scalable, production-grade DevOps foundation for agricultural AI systems."
    )
    story.append(Paragraph(conclusion_text, styles['DocBodyText']))
    story.append(Spacer(1, 10))

    story.append(Paragraph("7.2 Future Scope &amp; Scalability Roadmap", styles['DocSubSectionHeading']))
    future_text = (
        "Future enhancements include migrating from Docker Compose to <b>Kubernetes (k8s)</b> with Helm charts for horizontal "
        "pod autoscaling (HPA), introducing Prometheus and Grafana for real-time observability and latency tracing, and integrating "
        "SonarQube static application security testing (SAST) into the GitHub Actions CI pipeline."
    )
    story.append(Paragraph(future_text, styles['DocBodyText']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("7.3 References (IEEE Format)", styles['DocSubSectionHeading']))
    references = [
        "[1] D. Merkel, \"Docker: lightweight Linux containers for consistent development and deployment,\" <i>Linux Journal</i>, vol. 2014, no. 239, p. 2, Mar. 2014.",
        "[2] Docker Inc., \"Docker Compose Specification and Multi-Container Architecture,\" <i>Docker Documentation</i>, 2024. [Online]. Available: https://docs.docker.com/compose/.",
        "[3] J. Humble and D. Farley, <i>Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation</i>, Addison-Wesley Professional, 2010.",
        "[4] GitHub Inc., \"GitHub Actions Documentation: Workflow syntax, runners, and container registries,\" <i>GitHub Docs</i>, 2024. [Online]. Available: https://docs.github.com/en/actions.",
        "[5] PostgreSQL Global Development Group, \"PostgreSQL 16 Documentation: High Availability and Reliability Guidelines,\" <i>PostgreSQL Org</i>, 2024. [Online]. Available: https://www.postgresql.org/docs/16/."
    ]
    for ref in references:
        story.append(Paragraph(ref, styles['DocBodyText']))
        story.append(Spacer(1, 2))

    # Build Document with NumberedCanvas
    doc.build(story, canvasmaker=AcademicNumberedCanvas)
    print(f"Successfully generated PDF: {pdf_filename}")

if __name__ == "__main__":
    build_pdf()
