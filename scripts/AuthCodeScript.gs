var codes_url = '';

function main(e) {
  var values = e.values;
  var course = values[1];
  var email = values[2];
  var code = getCode(codes_url,course);

  var subject = 'ExCo ' + course + 'Authorization Code: ' + code;
  var message = 'Enter the code in the subjct line when registering for your ExCo';
  MailApp.sendEmail(email,subject,message);
};

// returns the last code in the list & deletes it from the spreadsheet
function getCode(codes_url,course) {
  var dataspreadsheet = SpreadsheetApp.openByUrl(codes_url);
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
