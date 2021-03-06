Delivery Plan
=============

This page describes the Delivery Plan for the project. 

The plan calls for an overall architecture design, which is executed in stages (mini-sprints, essentially). Each stage focuses on one component, with the overall plan ensuring each part fits together.

In this plan, there are three stages of delivery: This is because I would expect to be able to achieve each of these stages in roughly a day, once up to speed in a role.

*In this document*

1. List of Milestones
1. Delivery Detail
1. Risks & Mitigation

List of Milestones
------------------

1. Requirements restated
1. Delivery Plan created
1. Architectural design
1. Delivery stages:
    1. Foundations: Infrastructure, Database access, View
    1. Critical view: Admin side, tables, graphs, visualizations
    1. Survey view: 5 steps, next & previous, Ajax
1. Demonstration

Delivery Detail
---------------

#### Requirements restated

This milestone comprises the contents of the README file, which re-states the requirements.

This milestone is considered *achieved* on Monday 22 January.

#### Delivery Plan created

This milestone comprises the creation and approval of _this document_.

This milestone is expected 23-24 January.

#### Architectural design

The deliverables for this milestone are:

1. A file which describes the overall architecture of the solution, major platforms & third-party software, and how the components in each stage will fit together.
2. Feedback for that plan, incorporated revisions, and broad approval to proceed.

This milestone is expected 24-25 January.

#### Delivery

Each stage of delivery is essentially a mini-sprint, with requirements, coding, and release into the project. Mini-demonstrations of the state of the system at the conclusion of each stage are invited.

*Foundations*

During this stage, the infrastructure will be configured, the database configured, and the initial views made available to the *Admin* page and the *Survey* page. The database will be exposed through the built-in API views, and the server will be ready for use by the two pages through the web. There will be a *Hello* admin page, or a clear plan for it, and a *Hello* survey page, or a clear plan for it.

This stage is expected to last 1 day.

*Admin page*

During this stage the admin page will be developed, with the summary information and the list of survey responses. Sample data will need to be used to provide something for the system to display. The real-time updating aspect of the system will need to be in place, and simulated, but actual real time updating tests will not be possible until the *Survey* page.

This stage is expected to last 1-2 days.

*Survey page*

During this stage the survey page will be developed, showing the questions, steps, next/previous buttons and other end-user feedback.

The real-time updating feature of the *admin* page will be more easily testable once this is underway.

This third component of the system completes the end-to-end process of survey submission, storage, retrieval, display and analysis.

This stage is expected to last 1-2 days.

#### Demonstration

The live demonstration session will be scheduled upon successful delivery and is expected to last one hour or more.

#### Deliverables

1. Access to the code base. This is available at any time at [https://bitbucket.org/hotjar/dev-task-jeremy](https://bitbucket.org/hotjar/dev-task-jeremy)
1. Fully working demo. This will be available at [http://hotjar.jerjones.me](http://hotjar.jerjones.me) or [http://207.154.202.103](http://207.154.202.103)


Risks & Mitigation
------------------

1. _Failure to meet expectations_ for deliverables may result in solution which is not usable. This will be mitigated by frequent reviews of plans and code to ensure the final deliverables meet or exceed expectations. Risk of occurring: Medium
1. _Unexpected factors in first time components_ (namely API Star) may introduce delays to resolve. This will be mitigated by ensuring that the number of first-time components is as low as possible. Risk of occurring: Medium
1. _Others tbc_
