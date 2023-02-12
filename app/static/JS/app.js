
// Check picture's size prior to submitting:
function checkFileSize(theInput) {
    let parentDiv = document.getElementById('messageFileSizeDisapproved');
    if (parentDiv.hasChildNodes()){
        parentDiv.removeChild(parentDiv.firstChild);
    }
    
    if (theInput.files[0].size > 582000){
        
        let theP = document.createElement('p');
        theP.innerText = "Your image file is too big. Maximum image size: 582'000 bytes";
        parentDiv.append(theP);
        theInput.value= ""
    } else{
       
        if (parentDiv.hasChildNodes()) {
            parentDiv.removeChild(parentDiv.firstChild);
        }
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
    // let entry = new FormData
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
    // ADD REPLY LOGIC HERE AS WELL: isComment can be true or have a comment id
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
            }
        })
}