## How do I request a trial?

Submit the form on the website [trial page](/trial.html). Every applicant receives a dedicated demo environment pre-loaded with sample data relevant to their work.

## What is the difference between eTMF and CTMS?

eTMF manages **documents**: collection, review, approval, filing, and inspection readiness of the trial master file. CTMS manages **operations**: studies, sites, subjects, monitoring, and issues. Both share the study hierarchy data and together cover the full trial lifecycle.

## Where can I see the study hierarchy?

Open the **Study Info** tab. The **Studies** list shows all studies; open a study's detail page to drill down to study countries and study sites. See [Study Hierarchy](etmf/study-hierarchy.html).

## What is an EDL?

The EDL (Expected Document List) is the checklist of "what this TMF should contain", configured by admins via templates and automatically generated onto a study by the Plan Study action. See [EDL & Expected Documents](etmf/edl.html).

## When are documents automatically filed?

Approved documents in steady state are automatically filed into the corresponding Master File location. The filing location is determined by the document's TMF metadata and its expected document match. See [TMF Viewer](etmf/tmf-viewer.html).

## How do I check document completeness?

Open **TMF Homepage**, select a study, and review completeness, timeliness, and quality issue metrics with drill-down into individual documents. See [TMF Homepage](etmf/tmf-homepage.html).

## Where do I create and work clinical tasks?

On the eTMF side, create them under **Planning → Clinical Tasks**; on the CTMS side, work them under **Site Monitoring / Study Management** Clinical Tasks and Monitoring Follow Up Items. Assignees complete everything on the **My Tasks** page. See [Clinical Tasks](etmf/clinical-tasks.html).

## Where do administrators configure templates (EDL, milestones)?

Under **Admin Setup**: document types, Template EDLs, milestone master sets / sets / milestones / dependencies, template tasks, and reference models. A study applies them via **Plan Study**, which picks a master set and a Template EDL. See [Milestone Templates](etmf/template-milestones.html).

## What must be ready before starting a study?

While the study is in Candidate state, run **Plan Study** with a **Milestone Master Set**, a **Template EDL**, and the study start date; the system generates milestones and the expected document list. Then **Ready to Enroll** activates the study. See [Study Hierarchy](etmf/study-hierarchy.html).
