// This function sets up a trigger on the spreadsheet so that whenever
// the form is submitted, it calls the function 'emailCode' in 'trigger.gs'
function addTrigger() {
  var sheetId = PropertiesService.getScriptProperties().getProperty('sheetId');
  var sheet = SpreadsheetApp.openById(sheetId);
  ScriptApp.newTrigger('emailCode')
    .forSpreadsheet(sheet)
    .onFormSubmit()
    .create();
};

// This function is called by the python script via the Google Scripts API. It creates
// the form for instructors to request codes as well as the associated response spreadsheet.
function main(courses,codesId,passwordsId) {
  Logger.log(courses);
  Logger.log(codesId);
  var formId = createForm(courses);
  var sheetId = createSpreadsheet(formId);

  // saving IDs for documents to script properties for use by other functions.
  PropertiesService.getScriptProperties().setProperty('sheetId', sheetId);
  PropertiesService.getScriptProperties().setProperty('codes', codesId);
  PropertiesService.getScriptProperties().setProperty('passwords', passwordsId);
};

// ----------------------------------------------------------------------------------

var formTitle = "Authorization Code Request Form";
var formDescription = "Use this form to sent registration authorization codes to your students";

function createForm(courses) {
  var form = FormApp.create(formTitle)
  .setDescription(formDescription)
  .setCollectEmail(true);
  // form.requiresLogin(true); fix this!

  // create list of course numbers
  form.addListItem()
  .setTitle('Course Numbers')
  .setChoiceValues(courses)
  .setRequired(true);

  // add password box
  form.addTextItem()
  .setTitle('Enter Course Password')
  .setRequired(true);

  // preparing text validation
  var emailValidation = FormApp.createTextValidation()
  .requireTextMatchesPattern('^(\s?[^\s,]+@[^\s,]+\.[^\s,]+\s?,)*(\s?[^\s,]+@[^\s,]+\.[^\s,]+)$')
  .setHelpText('Type emails separated by commas')
  .build();

  // add email box (w/ text validation)
  form.addTextItem()
  .setTitle('Student Email Addresses')
  .setValidation(emailValidation)
  .setRequired(true);

  return form.getId();
};

function createSpreadsheet(formId) {
  // Open a form by ID and create a new spreadsheet.
  var form = FormApp.openById(formId);
  var ss = SpreadsheetApp.create('Auth Code Requests Log');

  // Update the form's response destination.
  form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());

  return ss.getId();
};
