from datetime import timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify
from apps.accounts.models import PortfolioItem, Skill, User
from apps.collaboration.models import CollaborationProject, JoinRequest, ProjectCategory, ProjectUpdate, TeamMember
from apps.communication.models import Conversation, Message, Notification
from apps.engagement.models import Report, Review
from apps.marketplace.models import Gig, GigCategory, Proposal

class Command(BaseCommand):
    help='Create realistic CampusCollab demonstration data.'

    @transaction.atomic
    def handle(self,*args,**options):
        today=timezone.localdate()
        skills=[]
        for name in ['Python','Django','JavaScript','HTML & CSS','UI/UX Design','React','Data Analysis','Machine Learning','Research Writing','Graphic Design','Digital Marketing','MySQL']:
            obj,_=Skill.objects.get_or_create(slug=slugify(name),defaults={'name':name});skills.append(obj)
        gig_categories=[]
        for name in ['Web Development','Design & Creative','Data & AI','Writing & Research','Marketing']:
            obj,_=GigCategory.objects.get_or_create(slug=slugify(name),defaults={'name':name});gig_categories.append(obj)
        project_categories=[]
        for name in ['Technology','Research','Social Impact','Business','Education']:
            obj,_=ProjectCategory.objects.get_or_create(slug=slugify(name),defaults={'name':name});project_categories.append(obj)

        admin,_=User.objects.get_or_create(email='admin@campuscollab.local',defaults={'username':'campusadmin','first_name':'Campus','last_name':'Admin','role':'admin','is_staff':True,'is_superuser':True})
        admin.role='admin';admin.is_staff=True;admin.is_superuser=True;admin.set_password('Admin123!');admin.save()
        student_specs=[
            ('samira@campuscollab.local','samira','Samira','Rahman','BRAC University','Computer Science','Full-stack developer building purposeful digital products.'),
            ('arif@campuscollab.local','arif','Arif','Hossain','North South University','EEE','IoT researcher and data enthusiast.'),
            ('nusrat@campuscollab.local','nusrat','Nusrat','Jahan','University of Dhaka','Marketing','Creative strategist focused on student-led brands.'),
            ('rafi@campuscollab.local','rafi','Rafi','Ahmed','BUET','CSE','Machine learning engineer and open-source contributor.'),
            ('tania@campuscollab.local','tania','Tania','Sultana','Jahangirnagar University','Statistics','Data analyst and research writer.'),
            ('sajid@campuscollab.local','sajid','Sajid','Khan','AIUB','Architecture','UI/UX and visual communication designer.'),
        ]
        students=[]
        for i,(email,username,first,last,uni,dept,headline) in enumerate(student_specs):
            user,_=User.objects.get_or_create(email=email,defaults={'username':username,'first_name':first,'last_name':last,'role':'student','profile_completed':True})
            user.username=username;user.first_name=first;user.last_name=last;user.role='student';user.profile_completed=True;user.set_password('Student123!');user.save()
            p=user.profile;p.university=uni;p.department=dept;p.headline=headline;p.location='Dhaka, Bangladesh';p.bio=f'{first} is an ambitious {dept} student who enjoys practical projects, teamwork and continuous learning.';p.availability='available' if i%3 else 'limited';p.github_url='https://github.com/example';p.linkedin_url='https://www.linkedin.com/';p.save()
            p.skills.set([skills[i%len(skills)],skills[(i+1)%len(skills)],skills[(i+3)%len(skills)],skills[(i+6)%len(skills)]])
            PortfolioItem.objects.get_or_create(owner=user,title=f'{first} Student Portfolio',defaults={'description':'A responsive portfolio showcasing academic and freelance work.','technologies':'HTML, CSS, JavaScript, Django','github_url':'https://github.com/example/campus-project','live_url':'https://example.com','completed_on':today-timedelta(days=30+i*5)})
            students.append(user)

        gig_specs=[
            ('Build a responsive club event website','Need a modern five-page website for a university tech club with event registration.',0,Decimal('12000'),14,[0,1,3]),
            ('Design a mobile app onboarding flow','Create polished UI screens and a clickable onboarding prototype for a student wellness app.',1,Decimal('8000'),10,[4,9]),
            ('Analyze survey data for research paper','Clean survey responses, run descriptive analysis and prepare clear charts for a research report.',2,Decimal('10000'),18,[6,8,11]),
            ('Create social media campaign assets','Design a campaign identity and twelve social posts for an upcoming campus competition.',1,Decimal('6500'),9,[9,10]),
            ('Django backend for campus marketplace','Implement authentication, CRUD APIs and MySQL models for an academic marketplace project.',0,Decimal('18000'),24,[0,1,11]),
            ('Literature review on sustainable logistics','Synthesize recent academic work and structure a concise literature review with references.',3,Decimal('9000'),16,[8,6]),
            ('Build an ML prototype for crop disease','Prepare a baseline image-classification notebook and document model performance.',2,Decimal('22000'),30,[0,7,6]),
            ('Landing page for student startup','Convert an approved design into a responsive landing page with subtle interactions.',0,Decimal('7500'),12,[2,3,4]),
        ]
        gigs=[]
        for i,(title,desc,cat,budget,days,skill_ids) in enumerate(gig_specs):
            gig,_=Gig.objects.get_or_create(owner=students[i%len(students)],title=title,defaults={'category':gig_categories[cat%len(gig_categories)],'description':desc,'budget':budget,'deadline':today+timedelta(days=days),'experience_level':'entry' if i%2==0 else 'intermediate','status':'open','is_featured':i<4})
            gig.skills.set([skills[j] for j in skill_ids]);gigs.append(gig)

        for i,gig in enumerate(gigs[:4]):
            applicant=students[(i+2)%len(students)]
            if applicant!=gig.owner:
                Proposal.objects.get_or_create(gig=gig,applicant=applicant,defaults={'cover_letter':f'I can deliver {gig.title.lower()} with a clear process, regular updates and attention to the approved design.','proposed_cost':gig.budget-Decimal('500'),'delivery_days':max(5,(gig.deadline-today).days-2),'milestones':'Discovery and scope\nFirst working draft\nReview and final delivery','status':'pending' if i>0 else 'accepted'})

        project_specs=[
            ('Smart Campus Navigation Assistant','Build an accessible navigation platform that helps new students find rooms, services and events.','startup',0,'Frontend developer, GIS researcher, Content designer',5,[0,1,2]),
            ('Bangla Handwriting Denoising Study','Compare image-processing and lightweight deep-learning approaches for cleaning handwritten documents.','research',1,'Computer vision researcher, Data annotator, Technical writer',4,[0,7,8]),
            ('Student Mental Wellness Survey','Design and analyze a cross-campus study on academic stress and support resources.','academic',2,'Survey designer, Data analyst, Research writer',6,[6,8]),
            ('Zero-Waste Campus Challenge','Create a measurable campaign and digital toolkit to reduce single-use waste across campus.','hackathon',2,'Product designer, Campaign strategist, Web developer',5,[3,4,10]),
            ('Peer Learning Exchange','Develop a platform where students host short peer-led learning sessions and skill swaps.','personal',4,'Django developer, UI designer, Community manager',4,[0,1,4]),
        ]
        projects=[]
        for i,(title,desc,ptype,cat,roles,size,skill_ids) in enumerate(project_specs):
            owner=students[(i+1)%len(students)]
            project,_=CollaborationProject.objects.get_or_create(owner=owner,title=title,defaults={'category':project_categories[cat%len(project_categories)],'project_type':ptype,'description':desc,'objectives':'Create a practical proof of concept, validate it with students, and document outcomes.','roles_needed':roles,'team_size':size,'start_date':today+timedelta(days=7),'end_date':today+timedelta(days=75+i*10),'work_mode':'hybrid' if i%2==0 else 'online','status':'recruiting','progress':15+i*8,'is_featured':i<4})
            project.skills.set([skills[j] for j in skill_ids]);TeamMember.objects.get_or_create(project=project,user=owner,defaults={'role':'Project owner'})
            member=students[(i+3)%len(students)]
            if member!=owner: TeamMember.objects.get_or_create(project=project,user=member,defaults={'role':roles.split(',')[0]})
            ProjectUpdate.objects.get_or_create(project=project,title='Project kickoff completed',defaults={'author':owner,'content':'The team aligned on scope, initial responsibilities and the first validation milestone.'})
            projects.append(project)

        JoinRequest.objects.get_or_create(project=projects[0],applicant=students[4],defaults={'role':'Content designer','message':'I have experience simplifying campus information and would love to help with content structure.'})
        conversation=Conversation.objects.filter(participants=students[0]).filter(participants=students[1]).first()
        if not conversation:
            conversation=Conversation.objects.create(project=projects[0]);conversation.participants.add(students[0],students[1])
        if not conversation.messages.exists():
            Message.objects.create(conversation=conversation,sender=students[0],body='Hi Arif! Your IoT background looks useful for the smart campus project.')
            Message.objects.create(conversation=conversation,sender=students[1],body='Thanks! I would be happy to discuss the prototype and sensor options.')
        Review.objects.get_or_create(reviewer=students[1],recipient=students[0],gig=gigs[0],defaults={'communication':5,'quality':5,'teamwork':5,'punctuality':4,'comment':'Clear communication, thoughtful work and a very reliable delivery process.'})
        Report.objects.get_or_create(reporter=students[2],target_type='gig',target_id=gigs[-1].pk,reason='Needs verification',defaults={'description':'Please verify whether the external link and project brief follow platform guidelines.'})
        for user in students:
            Notification.objects.get_or_create(recipient=user,title='Welcome to CampusCollab',defaults={'notification_type':'system','message':'Complete your profile, explore gigs and find your next collaboration.','url':'/dashboard/'})
        self.stdout.write(self.style.SUCCESS('Demo data ready. Admin: admin@campuscollab.local / Admin123! | Student: samira@campuscollab.local / Student123!'))
