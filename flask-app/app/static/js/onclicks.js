/* onclick functions for the app

Authors: Thomas Cleary,
*/

function confirmDelete(toDelete) {
  let msg = "Are you sure you want to delete " + toDelete + "?";
  let confimation = confirm(msg);
  console.log(confimation)
  return(confimation)
}
