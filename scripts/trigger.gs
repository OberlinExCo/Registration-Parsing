// This function is called whenever the form is submitted (presuming somebody called the 'addTrigger' function').
// It receives an event object 'e' with all the form data inside & handles the data appropriately.
// If you are having troubles with passwords, make sure the passwords are all cast as 'plain text'.
function emailCode(e) {
  var values = e.values;
  var requester = values[1];
  var course = values[2];
  var password = values[3];
  var email = values[4];

  // getting IDs for codes & passwords documents from script properties
  var codesId =  PropertiesService.getScriptProperties().getProperty('codes');
  var passwordsId = PropertiesService.getScriptProperties().getProperty('passwords');

  // Authenticating form request. This is crude, but it's something. If the password is incorrect, it sends an email
  // to exco@oberlin.edu and the requester so that the rest can be handled by a person.
  if(!Auth(passwordsId,course,password)){
    var subject = 'ExCo Auth Code Request Failure: ' + course;
    var message = 'Codes for EXCO' + course + ' were requested by ' + requester + ' for the following emails: ' + email;
    MailApp.sendEmail("exco@oberlin.edu," + requester,subject,message);
    throw new Error("Authentication for EXCO" + course + " has failed. Requester: " + requester + "; Emails: " + email);
  }

  // If authentication is successful, unique codes are sent to each of the emails listed on the form
  var emailArray = email.split(',');
  for (var i = 0; i < emailArray.length; i++) {
    var code = getCode(codesId,course);

    var subject = 'ExCo ' + course + ' Authorization Code';
    var message = 'Dear student\n\n Your authorization code for EXCO' + course + ' is: ' + code;
    MailApp.sendEmail(emailArray[i],subject,message);
  }
};

// -------------------------------------------------------

function Auth(passwordsId,course,password) {
  var dataspreadsheet = SpreadsheetApp.openById(passwordsId);
  var sheet = dataspreadsheet.getSheets()[0];
  var dict = sheet_to_dict(sheet);
  Logger.log(course);
  Logger.log(dict);
  var retVal = password === dict[course][0];
  Logger.log(retVal + " : " + password + " === " + dict[course][0]);
  return retVal;
}

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
