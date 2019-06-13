## The Wizard Knowledge Model 

The knowledge model is the encoding of all of the questions in the Data
Stewardship Wizard. It is the oldest component.

Work on the Knowledge Model started in the form of a mindmap connecting issues
on a wide range of subjects related to data management that could be covered
in a data management plan. It captured experience from researchers'
presentations, and information captured from workshops, meetings and papers.

The mind map can be found at: [https://doi.org/10.5281/zenodo.2614819](https://doi.org/10.5281/zenodo.2614819)

The Knowledge Model became a formal encoding of the information from the mind
map. Many of the nodes of the mind map have become questions in the wizard.
Other nodes as advice or guidance.
Questions coming from deeper layers of the mind map are conditional on the
higher layers of questions, and the relations are encoded in the knowledge
model. 

## The Structure of the Knowledge Model

1. It consists of a large core that is applicable everywhere, and
   localizations. The chapters and other global knowledge in the core are assembled in a
   "package". Each localization also requires a package.
2. It consists of chapters of questions that belong together
    * Each chapter could be presented as a tab in a user interface for the questionnaire.
3. The questions form hierarchies.
    * Most questions are only asked under the precondition that another question 
      has been answered in a specific way
    * "precondition" refers to a specific answer of a previously specified
      question. It is identified by the uuid of the answer.
    * only one precondition can be given for a question.
4. Questions that need to be posed as a series are usually asked in order of their definition.
    * If you want to define a question that needs to be posed before another
      question (it must be a question with the same precondition!), you should
      give it the "insertBefore" property, and specify a question uuid. The new 
      question will then be inserted before the specified referred question in the chain.
5. Localizations can be used to add specifics for a field of research, or to add 
   specifics for an institute or infrastructure.
6. Localizations can add new questions, or modify properties of core questions.
7. A question property specified in a localization /replaces/ that property completely.
    * If a localization needs to add experts, it should define the "addExperts" property.
    * If a localization needs to add answer options, it should define the "addAnswers" property.
    * If a localization needs to add references, it should define the "addReferences" property.
    * A localization can add the property "hidden": 1 to a question to remove 
      that question and all subquestions from the questionnaire.
    * [Should a localization be able to set a fixed answer to a question? An
      editable answer?]
8. Localizations can be stacked, and extend or overwrite each others changes
9. Chapters each have a uuid. Every localization can refer to the same chapters. 
10. If two localizations both want to define a new chapter (probably rare?), that 
    will require coordination.
11. Every localization has a namespace that differs from "core". 
    Each question is identified by a UUID.
12. If a localization wants to add a question, it is defined in the right
    chapter file in that localization namespace. Each question just gets a uuid.
13. If a localization wants to modify/augment a question it refers to that
    question from the other namespace by its uuid.
14. Questions have some additional properties:
     * "comment": A string for use of editors of the knowledge model, not used
       in the user interface for the questionnaire.
     * "phase": When the question really should be answered: 1: Before the
       project proposal is filed, 2: Before the DMP is filed, 3: Before the end
       of the project 4: Just nice to have, never required.
     * "references" and "experts".
        * "experts" on subjects are specific kinds of references with contact details. 
          They are added in localizations; the core does not have experts.
        * references of type "weblink" provide a "url" property and an optional "anchor" property
        * references of type "dmpbook" are direct links to chapters/sections in Barend Mons' book. 
          These may be used in the future to auto-regenerate new versions of the book
        * references of type "xref" are links to other questions of the questionnaire 
         (note for implementation: that may be a part of the questionnaire that is not active 
          because a negative answer was given elsewhere. Semantics to be figured out!)
      * "measures": references to how answering these questions contribute to
        metrics, like a prediction of how FAIR the data will become as a
        result of the documented Data Management practice.
15. Questions require different types of answers. Currently foreseen are "option", "list", 
    "string", "text"....
16. For questions of type "option":
     * a fixed number of selections are possible for the answer, presented as radio 
       buttons to the user. The user selects one.
     * A set of radiobuttons is good because it explicitly shows whether the user 
       has answered a question or not.
     * The possible answers are given in the "answers" property of the question.
     * Each answer has a "label"; often "Yes" and "No", in some cases "Skip" and
       "Explore" or equivalent are used.
     * For binary questions, the answer that does not require followup is preferred to be the first, 
       that is a "No" or "taken care of" answer.
     * Answers have a "uuid".
     * The "uuid" of the answer is also the reference for the "precondition" for a "followup" question.
     * [how to deal with refering to an expert?]
     * Each answer has a "responsetype" that is one of "ok", "followup" or "advice".
     * Answers of type "advice" have a "text" that will be shown if that answer is selected.
     * Answers can specify the "measure" for one or more metrics. Every metric
       measure that is specified will default to a weight of one, other
       "weight"s can be specified if desired.
17. For questions of "list" type:
     * No possible answers are given in the data model.
     * The user can type short free text items. "Add another one"....
     * Any followup questions need to be answered for each of the given free text answers.
18. For questions of type "string", "text":
     * No possible answers are given in the data model.
     * The user can type a short or long free text answer.
