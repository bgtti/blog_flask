//Closing alert message
function alertDisplayNone() {
    alert_div = document.getElementById("alertMsgJs");
    alert_div.classList.add("All-display-none")
}
//Alert messages JS: in base.html
function alert(message){
    alert_div = document.getElementById("alertMsgJs");
    alert_div.firstElementChild.textContent = message;
    alert_div.classList.remove("All-display-none")
    //add 'display none' class automatically after 20 seconds
    setTimeout(()=>{
        alertDisplayNone()
    }, 20000)
}

// Check user picture's size prior to submitting
// This will only alert the user, but not block the file submission!
function checkFileSize(theInput) {    
    if (theInput.files[0].size > 582000){
        alert("Your image file is too big. Maximum image size: 582'000 bytes")
    } 
}

// Check blog post picture's size prior to submitting
// This will only alert the user, but not block the file submission!
// Arguments: the picture object itself ("this" in the posts_submit_new.html file) and the_picture which
// can be "picture_v", "picture_h", or "picture_s"
// This function will return the size to a field in the form if the object is too big, or 0 if the object is within the 
// allowed file size limit
function checkFileSizeBlogPic(theInput, the_picture) {
    tellTheSizeField = document.getElementById(the_picture)
    console.log(theInput.files[0].size)
    console.log(tellTheSizeField)
    if (theInput.files[0].size > 1500000) {
        alert("Your image file is too big. Maximum image size: 1'500Kb")
        tellTheSizeField.value = theInput.files[0].size
    } else {
        tellTheSizeField.value = 0
    }
}

//action can be 'like' or 'bookmark'
function likeOrBookmark(postId, action) {
    let thumbsUp;
    let likesCount;
    let bookmark;
    if (action == "like"){
        thumbsUp = document.getElementById(`thumbs-up-${postId}`);
        likesCount = document.getElementById(`likes-count-${postId}`);
    } else {
        bookmark = document.getElementById(`bookmark-${postId}`);
    }
    url = action == "like" ? "/like_post/" + postId : "/bookmark_post/" + postId
    fetch(url, { method: "POST" })
        .then((res) => res.json())
        .then((data) => {
            if (action == "like" ){
                likesCount.innerHTML = data["likes"];
                has_liked = data["user_liked"];
                has_liked == "true" ? thumbsUp.classList.add("All-svg-clicked") : thumbsUp.classList.remove("All-svg-clicked");
            } else {
                has_bookmarked = data["user_bookmarked"];
                has_bookmarked == "true" ? bookmark.classList.add("All-svg-clicked") : bookmark.classList.remove("All-svg-clicked");
            }
        })
        .catch((e) => alert("Could not like/bookmark post"));
}

// reply form in posts.html to hide/show:
function toggleReplyForm(event, commentId){
    form = document.getElementById(`reply-form-${commentId}`)
    if (form.classList.contains("All-display-none")){
        event.target.classList.add("All-svg-clicked")
        form.classList.remove("All-display-none")
    } else {
        event.target.classList.remove("All-svg-clicked")
        form.classList.add("All-display-none")
    }
}

// Comment in Post or replies to comments in post(post.html)
// isComment can either be "true" or be a comment id
function commentOrReply(event, postId, isComment) {
    event.preventDefault()
    let theCommentOrReply;
    let commentOrReplyForm;
    let entry = {
        "comment": "",
        "reply": "",
        "commentId": ""
    }
    if (isComment == "true"){
        theCommentOrReply = document.getElementById(`comment-${postId}`);
        commentOrReplyForm = document.getElementById(`postCommentForm`);
        entry["comment"] = theCommentOrReply.value
    } else{
        theCommentOrReply = document.getElementById(`reply-area-${isComment}`);
        commentOrReplyForm = document.getElementById(`postReplyForm-${isComment}`);
        entry["reply"] = theCommentOrReply.value
        entry["commentId"] = `${isComment}`
    }
    if (theCommentOrReply.value == "") {
        console.warn("Empty comment cannot be sent")
        return
    }
    commentOrReplyForm.reset()
    let thePId;
    isComment == "true" ? thePId = `Msg-sent` : thePId = `Reply-sent-${isComment}`
    let msgSentP = document.getElementById(thePId);
    url = `/comment_post/${postId}`
    fetch(url, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(entry),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then((res) => res.json())
        .then((data) => {
            if (data['message'] == "Comment empty") {
                msgSentP.textContent == "You cannot send an empty comment or reply. Request failed."
            } else {
                msgSentP.classList.remove("All-display-none")
                isComment == "true" ? alert("Comment sent! Refresh the page to see the changes") : alert("Reply sent! Refresh the page to see the changes")

            }
        })
}

// delete comments or replies
// Comment in Post or replies to comments in post(post.html)
// isComment can either be "true" or be a comment id
function deleteCommentOrReply(event, postId, isComment, commentOrReplyId) {
    event.preventDefault()
    let theCommentOrReply;
    let entry = {
        "commentId": "",
        "replyId": ""
    }
    if (isComment == "true") {
        theCommentOrReply = document.getElementById(`comment-id-${commentOrReplyId}`);
        entry["commentId"] = `${commentOrReplyId}`
    } else {
        theCommentOrReply = document.getElementById(`reply-id-${commentOrReplyId}`);
        entry["replyId"] = `${commentOrReplyId}`
    }
    let thePId;
    isComment == "true" ? thePId = `p-parent-of-${commentOrReplyId}-comment` : thePId = `p-parent-of-${commentOrReplyId}-reply`
    let deletedMsgP = document.getElementById(thePId);
    url = `/delete_comment_or_reply/${postId}`
    fetch(url, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(entry),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then((res) => res.json())
        .then((data) => {
            console.log((deletedMsgP.firstElementChild))
            deletedMsgP.removeChild(deletedMsgP.lastElementChild)
            if (data['message'] == "Successfully deleted") {
                deletedMsgP.firstElementChild.textContent = "Deleted!"
                alert("Successfully deleted! Refresh the page to see the changes.")
            } else {
                deletedMsgP.firstElementChild.textContent = "Request failed."
            }
        })
}