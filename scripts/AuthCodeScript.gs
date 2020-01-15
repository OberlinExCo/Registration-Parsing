var formTitle = "Authorization Code Request Form";
var formDescription = "Use this form to sent registration authorization codes to your students";

function main(courses,codesId,passwordsId) { // do we want to use URL for codes document?
  Logger.log(courses);
  Logger.log(codesId);
  var formId = createForm(courses);
  var sheetId = createSpreadsheet(formId);
  PropertiesService.getScriptProperties().setProperty('sheetId', sheetId);
  PropertiesService.getScriptProperties().setProperty('codes', codesId);
  PropertiesService.getScriptProperties().setProperty('passwords', passwordsId);
};

function addTrigger() { // idk if this is the way to do this
  var sheetId = PropertiesService.getScriptProperties().getProperty('sheetId');
  var sheet = SpreadsheetApp.openById(sheetId);
  ScriptApp.newTrigger('emailCode')
    .forSpreadsheet(sheet)
    .onFormSubmit()
    .create();
};

function emailCode(e) {
  var values = e.values;
  var course = values[1];
  var password = values[2];
  var email = values[3];
  var requester = values[4];

  var codesId =  PropertiesService.getScriptProperties().getProperty('codes');
  var passwordsId = PropertiesService.getScriptProperties().getProperty('passwords');

  if(!Auth(passwordsId,course,password)){
    var subject = 'ExCo Auth Code Request Failure: ' + course;
    var message = 'Codes for EXCO' + course + ' were requested by ' + requester + ' for the following emails: ' + email;
    MailApp.sendEmail("exco@oberlin.edu," + requester,subject,message);
    throw new Error("Authentication for EXCO" + course + " has failed. Requester: " + requester + "; Emails: " + email);
  }

  var emailArray = email.split(',');

  for (var i = 0; i < emailArray.length; i++) {
    var code = getCode(codesId,course);

    var subject = 'ExCo ' + course + ' Authorization Code';
    var message = 'Dear student\n\n Your authorization code for EXCO' + course + ' is: ' + code;
    MailApp.sendEmail(emailArray[i],subject,message);
  }
};

function Auth(passwordsId,course,password) {
  var dataspreadsheet = SpreadsheetApp.openById(passwordsId);
  var sheet = dataspreadsheet.getSheets()[0];
  var dict = sheet_to_dict(sheet);
  var retVal = password === dict[course][0];
  Logger.log(retVal + " : " + password + " === " + dict[course][0]);
  return retVal;
}

function createForm(courses) {
  var form = FormApp.create(formTitle)
  .setDescription(formDescription)
  .collectsEmail(true);
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

// returns the last code in the list & deletes it from the spreadsheet
function getCode(codesId,course) {
  var dataspreadsheet = SpreadsheetApp.openById(codesId);
  var sheet = dataspreadsheet.getSheets()[0];
  var dict = sheet_to_dict(sheet);
  var last_index = dict[course].length - 1;
  Logger.log(dict[course][last_index]);
  sheet.createTextFinder(dict[course][last_index]).replaceAllWith('');
  return dict[course][last_index];
};

// modified from: https://gist.github.com/dangtrinhnt/e041557101dac07bbdae
// thedict = {'<col_header0>': ['<row0>','<row1>',...], '<col_header1>': ['<row0', '<row1>',...]...}
function sheet_to_dict(sheet) {
  var result_dict = {};
  var cols = sheet.getLastColumn();
  var rows = sheet.getLastRow();

  var data = sheet.getDataRange().getValues();
  // data[row][col]

  for (var r = 0; r < rows; r++) {
    var header = data[r][0];
    var row_data_list = [];
    for(var c = 1; c < cols; c++) {
      var cell_data = data[r][c];
      if(cell_data !== ''){
        row_data_list.push(cell_data);
      }
    }
    if (row_data_list.length > 0) {
      result_dict[data[r][0]] = row_data_list;
    }
  }
  return result_dict;
}
