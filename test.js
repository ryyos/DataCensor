var dppCalled = false;
var fdsCookie;
function callPostDownload() {
  if (!dppCalled) {
    checkDownloadStarted();
  }
  dppCalled = true;
  return true;
}
function checkDownloadStarted() {
  var a = readD3Cookie();
  if (a == "INITIALIZED") {
    clearD3Cookie();
    startRedirectToD3();
  } else {
    setTimeout("checkDownloadStarted()", 500);
  }
}
function clearD3Cookie() {
  Cookies.erase(fdsCookie, "/", $(".jsCookieDomain").val());
}
function readD3Cookie() {
  Cookies.read();
  return Cookies[fdsCookie];
}
function startRedirectToD3() {
  document.redirectToD3Form.submit();
}
$(function () {
  $("a.linkShowD3")
    .click(function () {
      callPostDownload();
    })
    .mousedown(function (a) {
      if (a.which == 2) {
        callPostDownload();
      }
    });
  fdsCookie = "fds" + $(".jsFileId").val();
  clearD3Cookie();
});
