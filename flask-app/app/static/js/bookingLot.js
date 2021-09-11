/* Functions to update selected booking on booking pages

Authors: Thomas Cleary,
*/

function addBuffers() {
  let timetables = document.getElementsByClassName("timetable");

  for (let table of timetables) {
    let rows = table.getElementsByTagName('tr');
    for (let row of rows) {
      let cells = row.getElementsByClassName("timeslot");
      for (let i = 0; i < cells.length; i++) {
        let cell = cells[i];
        if (cell.classList.contains("timeslot-green")) {
          if (i > 0) {
            if (cells[i-1].classList.contains("timeslot-red")) {
              cell.classList.remove("timeslot-green");
              cell.classList.add("timeslot-orange");
            }
          }
          if (i < cells.length-1) {
            if (cells[i+1].classList.contains("timeslot-red")) {
              cell.classList.remove("timeslot-green");
              cell.classList.add("timeslot-orange");
            }
          }
        }
      }
    }
  }
}


function turnCellOn(cell) {
  cell.classList.remove("timeslot-green");
  cell.classList.add("timeslot-yellow");
}


function turnCellOff(cell) {
  cell.classList.remove("timeslot-yellow");
  cell.classList.add("timeslot-green");
}


function isCellOn(cell) {
  return (cell.classList.contains("timeslot-yellow"));
}


function selectTimeslot(cellID) {
  let clickedCell = document.getElementById(cellID);

  // turn the cell on
  if (clickedCell.classList.contains("timeslot-green")) {
    // TURN OFF OTHER CELLS NOT IN THIS ROW
    updateTimetables(clickedCell);
  }
  // turn the cell off
  else {
    updateClickedRow(clickedCell);
  }

  updatePageBanner(clickedCell);
}


function updateTimetables(clickedCell) {
  let timetables = document.getElementsByClassName("timetable");
  let clickedRow = clickedCell.parentElement;

  for (let table of timetables) {
    let rows = table.getElementsByTagName("tr");

    for (let row of rows) {
      let cells = row.getElementsByTagName("td");

      // turn off cells not in the clicked row
      if (!(row == clickedRow)) {
        for (let cell of cells) {
          if (cell.classList.contains("timeslot-yellow")) {
            turnCellOff(cell);
          }
        }
      }

      // turn on cells in between previous selection and this clicked cell
      else {
        let turnOn = [];

        let foundClicked = false;
        let foundStart   = false;
        let logCells     = false;

        for (let cell of cells) {
          if (cell == clickedCell) {
            foundClicked = true;
            logCells = true;
            turnCellOn(cell); 
          }
          else if (!foundStart && cell.classList.contains("timeslot-yellow")) {
            foundStart = true;
            logCells = true;
          }

          if (logCells) {
            if (!isCellOn(cell)) {
              turnOn.push(cell);
            }
          }

          if (foundClicked && foundStart) {
            break;
          }
        }

        if (foundStart) {
          for (let cell of turnOn) {
            turnCellOn(cell);
          }
        }
      }
    }
  }
}

// turn of cells to left or right of clicked cell depending on which side has more
// turn off side with less
function updateClickedRow(clickedCell) {
  let clickedRow = clickedCell.parentElement;

  let leftOn =  [];
  let rightOn = [];
  let addLeft = true;

  let cells = clickedRow.getElementsByTagName("td");

  for (let cell of cells) {
    if (cell == clickedCell) {
      addLeft = false;
      continue;
    }
    else if (cell.classList.contains("timeslot-yellow")) {
      if (addLeft) {
        leftOn.push(cell);
      }
      else {
        rightOn.push(cell);
      }
    }
  }

  turnOffCells = [];
  if (leftOn.length < rightOn.length) {
    turnOffCells = leftOn;
  }
  else {
    turnOffCells = rightOn;
  }

  for (let cell of turnOffCells) {
    turnCellOff(cell);
  }
  turnCellOff(clickedCell);

}


function updatePageBanner(clickedCell) {
  let clickedRow = clickedCell.parentElement;

  let bookingTitleSpan = document.getElementById("selected-booking");
  let confirmBookingBtn = document.getElementById("confirm-button");
  let onCells = getOnCells(clickedRow);

  if (onCells.length > 0) {
    let queryArgs = getQueryArgs(clickedRow, onCells);
    let confirmURL = buildConfirmURL(queryArgs);
    let bookingTitle = getBookingTitle(queryArgs);

    bookingTitleSpan.innerHTML = bookingTitle;
    confirmBookingBtn.href = confirmURL;

    confirmBookingBtn.style.visibility = "visible";
  }
  else {
    bookingTitleSpan.innerHTML = "No Booking Selected";
    confirmBookingBtn.style.visibility = "hidden";
  }
}


function getOnCells(clickedRow) {
  let cells = clickedRow.getElementsByClassName("timeslot");

  let onCells = [];
  for (let cell of cells) {
    if (cell.classList.contains("timeslot-yellow")) {
      onCells.push(cell);
    }
  }
  return onCells;
}


function getQueryArgs(clickedRow, onCells) {
  let bayInfo = clickedRow.id.split("-");
  let lotNum = bayInfo[0].replace( /^\D+/g, '');
  let bayNum = bayInfo[1].replace( /^\D+/g, '');

  let date = document.querySelector('[id^="date-"]').id.split("-")[1].split("/");

  let start = onCells[0].id.split("-")[2].replace(/^\D+/g, '');
  let end   = onCells[onCells.length-1].id.split("-")[2].replace(/^\D+/g, '');

  return {
    "lot_num" : lotNum,
    "bay_num" : bayNum,
    "day"    : date[0],
    "month"  : date[1],
    "year"   : date[2],
    "start"  : start,
    "end"    : end
  };
}


function buildConfirmURL(queryArgs) {
  let url = new URL("/bookings/confirm", document.location);
  for (let key in queryArgs) {
    url.searchParams.append(key, queryArgs[key]);
  }
  return url.toString();
}


function getBookingTitle(queryArgs) {
  let titleTemplate = "Lot {0} Bay {1}  -  {2}/{3}/{4}  -  {5} to {6}  ";

  let params = [];
  for (key in queryArgs) {
    params.push(queryArgs[key]);
  }

  // change timeslots to actual time
  params[5] = getTime(params[5]);
  params[6] = getTime(parseInt(params[6]) + 1);

  return formatString(titleTemplate, params);
}

function formatString(str, params) {
  for (let i = 0; i < params.length; i++) {
      var reg = new RegExp("\\{" + i + "\\}", "gm");
      str = str.replace(reg, params[i]);
  }
  return str;
}


function getTime(timeslot) {
  let times = getTimes(34);
  return times[timeslot];
}


function getTimes(numSlots) {
  let hour = 8;
  let minutes = 45;

  let times = [];

  for (let i = 0; i < numSlots; i++) {
    if (minutes === 0) {
      minutes = "00";
    }

    let time = hour + ":" + minutes;
    
    if (hour < 12) {
      time += " AM";
    }
    else {
      time += " PM";
    }

    minutes = parseInt(minutes);
    minutes += 15;
    if (minutes === 60) {
      minutes = 0;
      hour += 1;
    }

    times.push(time);
  }

  return times;
}