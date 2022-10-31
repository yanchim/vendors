// ==UserScript==
// @name         Rule34 Image Downloader
// @namespace    https://tampermonkey.net/
// @version      0.1
// @description  easier download images from rule34.xxx
// @author       yanchi
// @match        https://rule34.xxx/*
// @icon         https://www.google.com/s2/favicons?domain=rule34.xxx
// @connect      https://rule34.xxx/*
// @grant        GM_download
// @grant        GM_xmlhttpRequest
// ==/UserScript==

function getOriginalImageUrlFromSideBarList(lists) {
  let optionLinkHTML;
  lists.forEach((list) => {
    if (list.innerText.indexOf("Options") !== -1) {
      optionLinkHTML = list;
    }
  });

  let origLink;
  optionLinkHTML.querySelectorAll("a").forEach((link) => {
    if (link.href.indexOf("image") !== -1) {
      origLink = link.href;
    }
  });

  return origLink;
}

function getFilenameFromLink(link) {
  let result = link.slice(link.lastIndexOf("/") + 1, link.lastIndexOf("?"));
  return result;
}

function downloadImage(image_page_link) {
  let xhr = new XMLHttpRequest();
  xhr.open("GET", image_page_link, true);
  xhr.send();
  xhr.onreadystatechange = () => {
    if (xhr.readyState == 4 && xhr.status == 200) {
      let tmp = document.createElement("div");
      tmp.innerHTML = xhr.responseText;

      let list = tmp.querySelectorAll("div.link-list");
      let link = getOriginalImageUrlFromSideBarList(list);

      onDownload(link);
    }
  };
}

function viewImage(image_page_link) {
  let xhr = new XMLHttpRequest();
  xhr.open("GET", image_page_link, true);
  xhr.send();
  xhr.onreadystatechange = () => {
    if (xhr.readyState == 4 && xhr.status == 200) {
      let tmp = document.createElement("div");
      tmp.innerHTML = xhr.responseText;

      let list = tmp.querySelectorAll("div.link-list");
      let link = getOriginalImageUrlFromSideBarList(list);

      window.open(link);
    }
  };
}

function addDownloadLinkOnViewPage() {
  let imageSublinks = document.querySelector("h4.image-sublinks");
  let downloadLink = document.createElement("button");
  downloadLink.innerHTML = "Download";

  let linkLists = document.querySelectorAll("div.link-list");
  let link = getOriginalImageUrlFromSideBarList(linkLists);

  downloadLink.onclick = () => {
    onDownload(link);
  };
  imageSublinks.append(" | ");
  imageSublinks.append(downloadLink);
}

function onDownload(link) {
  console.log(new Date().toLocaleString(), link);
  filename = getFilenameFromLink(link);
  GM_download({ url: link, name: filename });
}

(function () {
  "use strict";

  let contentDiv = document.querySelector("div.content div");
  let posts = contentDiv.querySelectorAll("span");

  if (document.location.href.indexOf("s=view") !== -1) {
    addDownloadLinkOnViewPage();
    // skip the following steps
    return;
  }

  // Deal individual image
  posts.forEach((post) => {
    let link = post.querySelector("a").href;

    let downloadButton = document.createElement("button");
    downloadButton.innerHTML =
      "<p style='margin: 2px; font-size: 12px;'> Download </p>";
    downloadButton.onclick = function () {
      downloadImage(link);
    };
    post.prepend(downloadButton);

    post.prepend(" | ");

    let viewButton = document.createElement("button");
    viewButton.innerHTML =
      "<p style='margin: 2px; font-size: 12px;'> View </p>";
    viewButton.onclick = function () {
      viewImage(link);
    };
    post.prepend(viewButton);
  });

  // Download all images on the page
  let buttonAll = document.createElement("button");
  buttonAll.style = "width: 100%";
  buttonAll.innerHTML =
    "<p style='margin: 2px; font-size: 16px;'> Download All </p>";
  buttonAll.onclick = function () {
    posts.forEach((post) => {
      let link = post.querySelector("a").href;
      downloadImage(link);
    });
  };
  document.querySelector("div.content").prepend(buttonAll);
})();
