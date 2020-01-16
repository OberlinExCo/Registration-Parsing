function addTrigger() { // idk if this is the way to do this
  var sheetId = PropertiesService.getScriptProperties().getProperty('sheetId');
  var sheet = SpreadsheetApp.openById(sheetId);
  ScriptApp.newTrigger('emailCode')
    .forSpreadsheet(sheet)
    .onFormSubmit()
    .create();
};

function main(courses,codesId,passwordsId) { // do we want to use URL for codes document?
  Logger.log(courses);
  Logger.log(codesId);
  var formId = createForm(courses);
  var sheetId = createSpreadsheet(formId);
  PropertiesService.getScriptProperties().setProperty('sheetId', sheetId);
  PropertiesService.getScriptProperties().setProperty('codes', codesId);
  PropertiesService.getScriptProperties().setProperty('passwords', passwordsId);
};

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
