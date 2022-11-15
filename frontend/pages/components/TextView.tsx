import styled from "@emotion/styled";
import React from "react";
import { useSearchParams } from "react-router-dom";
import { Input, Textarea } from "theme-ui";
import { ApiFetch, getCurrentUser, getPermission } from "../../App";
import { APIcall } from "../../interfaces";
import { theme } from "../../theme";
import CommentContext from "../commentContext";
import { StyledButton } from "../GlobalProps";
import AuthorView from "./AuthorView";
import ReactTooltip from 'react-tooltip';

// Declaring and typing our props
interface Props {
  text: string,
  private?: boolean,
  anonymous?: boolean,
  heading?: string,
  author: number,
  id: number,
  commentId?: number,
  reacts: number,
  userReacted: boolean,
  type: "post" | "comment" | "reply",
  tags?: number[],
  queue?: string,
  answered?: number | null,
  closed?: boolean,
  accepted?: boolean,
  deleted?: boolean,
  reported?: boolean,
  showCloseButton?: boolean,
  showAcceptButton?: boolean,
  showDeleteButton?: boolean,
  showReportButton?: boolean
  showUnreportButton?: boolean
}

const StyledText = styled.div`
  border-radius: 2px;
  overflow: hidden;
  h1 {
    margin-top: 0px;
  }
  hr {
    color: white;
  }
  p {
    margin-top: 0;
  }
  h1 {
    margin-bottom: 10px;
  }
`
const StyledPost = styled.div`
`
const StyledBorder = styled.div`
  height: 1px;
  border-bottom: black;
`

const StyledReply = styled.div`
  margin-top: 5px;
  display: flex;
  content-align: center;
  button {
    border: 1px solid black;
    height: 40px;
  }
  input {
    border-right: 0;
    border-radius: 10px 0 0 10px;
    height: 40px;
  }  
`
const StyledReplyButton = styled(StyledButton)`
    border-radius: 0 10px 10px 0;
`
const StyledPostButton = styled(StyledButton)`
  border-left: 0;
  border-radius: 0 10px 10px 0;
`
const InactiveReactButton = styled(StyledButton)`
  padding: 5px;
  margin-right: 5px;
  background-color: darkgrey;
  color: white;
`
const ActiveReactButton = styled(InactiveReactButton)`
  background-color: ${theme.colors?.primary};
  font-weight: 900;
`
const ActiveCloseButton = styled(InactiveReactButton)`
  background-color: #2574f5;
`
const ActiveAcceptButton = styled(InactiveReactButton)`
  background-color: #7de37d;
`

const DeleteButton = styled(InactiveReactButton)`
  background-color: #ff8080;
`
const ReportButton = styled(InactiveReactButton)`
  background-color: #FF0000;
`
const ActiveReportButton = styled(InactiveReactButton)`
  background-color: black;
`

const OptionsBar = styled.div`
  display: flex;
  justify-content: space-between;
  margin: 0;
`

const Private = styled.div`
  margin-left: 10px;
  background-color: lightgrey;
  padding: 5px;
  border-radius: 10px;
  font-weight: 700;
  display: flex;
  align-items: center;
  text-align: center;
  max-width: 100px;
  height: 30px;
`
const Anonymous = styled(Private)`
  max-width: 130px;
`
const Queue = styled.div`
  text-align: center;
  font-weight: 500;
`

const StyledAnonymous = styled.a`
  text-decoration: underline;
  &:hover {
    cursor: pointer;
    font-weight: 700;
  }
`
const Row = styled.span`
  display:flex;
  padding-bottom: 10px;
`
const Col = styled.span`
  display:flex;
  flex-direction: column;
`

// Exporting our example component
const TextView = (props: Props) => {
  const [inputText, setInputText] = React.useState<string>();
  const [toggleReply, setToggleReply] = React.useState<boolean>(false);
  const [editHeading, setEditHeading] = React.useState<string>(props.heading as string);
  const [editText, setEditText] = React.useState<string>(props.text as string);
  const [toggleEdit, setToggleEdit] = React.useState<boolean>(false);
  const { commentCount, setCommentCount } = React.useContext(CommentContext);
  let [searchParams, setSearchParams] = useSearchParams();
  
  function updatePosts() {
    const postId = searchParams.get('postId') as string;
    if (postId.startsWith('0')) {
      setSearchParams({postId: postId.slice(1)})
    } else {
      setSearchParams({postId: '0'+postId})
    }
  }


  const routes = {
    "post": ["browse/post_view/comment", "✋ ", "browse/post_view/react", "post_id", "post_id", "browse/post_view/edit"],
    "comment": ["browse/comment_view/reply", "👍 ", "browse/comment_view/react", "comment_id", "comment_id", "browse/comment_view/edit"],
    "reply": ["browse/comment_view/reply", "👍 ", "browse/reply_view/react", "comment_id", "reply_id", "browse/reply_view/edit"],
  } 
  let heading = <></>;
  let author = <></>;
  let closed = <></>;
  let answered = <></>;
  let reported = <></>;
  let deleted = <></>;
  if (props.closed) {
    closed = <>
    <ReactTooltip place="top" type="dark" effect="solid"/>
    <span data-tip="Post has been closed by a moderator. Edit post based on comment feedback">🔒{' '}</span>
    </>
  }
  if (props.answered) {
    answered = <>
    <ReactTooltip place="top" type="dark" effect="solid"/>
    <span data-tip="Post has been marked as answered">✅{' '}</span>
    </>
  }
  if (props.reported && props.showUnreportButton) {
    reported = <>
    <ReactTooltip place="top" type="dark" effect="solid"/>
    <span data-tip="Post has been reported">❗</span>
    </>
  }
  if (props.deleted) {
    deleted = <>
    <ReactTooltip place="top" type="dark" effect="solid"/>
    <span data-tip="Post has been deleted">🗑️{' '}</span>
    </>
  }

  if (props.heading) {
    heading = <h1>{closed}{answered}{reported}{deleted}{props.heading}</h1>
  }

  if (props.author) {
    author = <AuthorView userId={props.author}/>;
  } else if (props.type === "post" && props.anonymous) {
    author = <StyledAnonymous>Anonymous</StyledAnonymous>
  }


  let tags = <></>;
  if (props.tags) {
    tags = <>Tags: {props.tags.map((each) => {return <>{each} </>})}</>
  }

  function react() {
    const key = routes[props.type][4];
    const call : APIcall = {
      method: "PUT",
      path: routes[props.type][2],
      body: {key: props.id}
    }
    call.body[key] = props.id;
    ApiFetch(call).then(
      () => {
        setCommentCount(commentCount + 1);
      }
    );
  }
  async function close_post() {
    const call : APIcall = {
      method: "PUT",
      path: "browse/post_view/close",
      body: {post_id: props.id}
    }
    await ApiFetch(call);
    setCommentCount(commentCount + 1);
    updatePosts();
  }
  async function answer_post() {
    const call : APIcall = {
      method: "PUT",
      path: "browse/comment_view/accept",
      body: {comment_id: props.id}
    }
    await ApiFetch(call);
    setCommentCount(commentCount + 1);
    updatePosts();
  }
  async function delete_post() {
    const call : APIcall = {
      method: "DELETE",
      path: "browse/post_view/delete",
      params: {post_id: props.id.toString()}
    }
    await ApiFetch(call);
    setCommentCount(commentCount + 1);
    updatePosts();
  }
  async function delete_comment() {
    const call : APIcall = {
      method: "DELETE",
      path: "browse/comment_view/delete",
      params: {comment_id: props.id.toString()}
    }
    await ApiFetch(call);
    setCommentCount(commentCount + 1);
    updatePosts();
  }
  async function delete_reply() {
    const call : APIcall = {
      method: "DELETE",
      path: "browse/reply_view/delete",
      params: {reply_id: props.id.toString()}
    }
    await ApiFetch(call);
    setCommentCount(commentCount + 1);
    updatePosts();
  }

  async function report_post() {
    const call : APIcall = {
      method: "PUT",
      path: "browse/post_view/report",
      body: {"post_id": props.id}
    }
    console.log(call)
    await ApiFetch(call);
    setCommentCount(commentCount + 1);
    updatePosts();
  }
  async function unreport_post() {
    const call : APIcall = {
      method: "PUT",
      path: "browse/post_view/unreport",
      body: {"post_id": props.id}
    }
    await ApiFetch(call);
    setCommentCount(commentCount + 1);
    updatePosts();
  }


  const reply = (
  <StyledReply>
    <Input placeholder="Reply" value={inputText} onChange={(e)=>setInputText(e.target.value)} ></Input>
    <ActiveReactButton onClick={(e) => {
        const call : APIcall = {
          method: "POST",
          path: routes[props.type][0],
          body: {"text": inputText}
        }
        if (props.commentId) {
          call.body[routes[props.type][3]] = props.commentId;
        } else {
          call.body[routes[props.type][3]] = props.id;
        }
        ApiFetch(call).then(()=>{
          setCommentCount(commentCount + 1);
          setToggleReply(false);
        });
    }}>Post</ActiveReactButton>
  </StyledReply>)
  const replyButton = (<><ReactTooltip place="top" type="dark" effect="solid"/><InactiveReactButton data-tip="Reply" onClick={() => setToggleReply(true)}>↩️</InactiveReactButton></>);
  const activeReplyButton = (<ActiveReactButton onClick={() => setToggleReply(false)}>↩️</ActiveReactButton>);
  const editBox = (
    <>
      {props.type === "post" ?
      <>
        Tags Todo
        <Textarea value={editHeading} onChange={(e) => setEditHeading(e.target.value)}></Textarea> 
        {/*<Textarea value={editTags} onChange={(e) => setEditTags(e.target.value)}></Textarea>*/}
      </>: <></>
      }
      <Textarea value={editText} onChange={(e) => setEditText(e.target.value)}></Textarea>
      <StyledButton onClick={() => {
        const call : APIcall = {
          method: "PUT",
          path: routes[props.type][5],
          body: { text: editText, }
        }
        call.body[routes[props.type][4]] = props.id;
        if (props.type === "post") {
          call.body.tags = (props.tags ? props.tags : []);
          call.body.heading = editHeading;
        }
        ApiFetch(call).then(
          () => {
            setToggleEdit(false);
            setCommentCount(commentCount + 1);
            updatePosts();
          }
        );
      }}>Post</StyledButton>
    </>
  );
  const editButton = (<>
  <ReactTooltip place="top" type="dark" effect="solid"/>
  <InactiveReactButton data-tip="Edit" onClick={() => setToggleEdit(true)}>✏️</InactiveReactButton>
  </>);
  const activeEditButton = (<ActiveReactButton onClick={() => setToggleEdit(false)}>✏️</ActiveReactButton>);
  const reactButton = (<>
    <ReactTooltip place="top" type="dark" effect="solid"/>
    <InactiveReactButton data-tip={props.type === "post" ? "Me too!" : "Thanks!"} onClick={() => react()}>{routes[props.type][1]} <>{
            props.reacts }</></InactiveReactButton>
  </>);
  const activeReactButton = (<>
    <ReactTooltip place="top" type="dark" effect="solid"/>
    <ActiveReactButton data-tip="Unreact" onClick={() => react()}>{routes[props.type][1]} <>{
            props.reacts }</></ActiveReactButton>
  </>);
  const closeButton = (<>
    <ReactTooltip place="top" type="dark" effect="solid"/>
    <InactiveReactButton data-tip="Close Post" onClick={() => close_post()}>🔒</InactiveReactButton>
  </>)
  const activeCloseButton = (<>
    <ReactTooltip place="top" type="dark" effect="solid"/>
    <ActiveCloseButton data-tip="Unclose Post" onClick={() => close_post()}>🔒</ActiveCloseButton>
  </>)
  const acceptButton = (<>
    <ReactTooltip place="top" type="dark" effect="solid"/>
    <InactiveReactButton data-tip="Mark as answered" onClick={() => answer_post()}>✅</InactiveReactButton>
  </>)
  const activeAcceptButton = (<>
    <ReactTooltip place="top" type="dark" effect="solid"/>
    <ActiveAcceptButton data-tip="Unmark as answered" onClick={() => answer_post()}>✅</ActiveAcceptButton>
  </>)
  const deleteButton = (<>
    <ReactTooltip place="top" type="dark" effect="solid"/>
    <DeleteButton data-tip="Delete post" onClick={() => delete_post()}>🗑️</DeleteButton>
  </>)
  const deleteCommentButton = (<>
    <ReactTooltip place="top" type="dark" effect="solid"/>
    <DeleteButton data-tip="Delete comment" onClick={() => delete_comment()}>🗑️</DeleteButton>
  </>)
  const deleteReplyButton = (<>
    <ReactTooltip place="top" type="dark" effect="solid"/>
    <DeleteButton data-tip="Delete reply" onClick={() => delete_reply()}>🗑️</DeleteButton>
  </>)

  const reportButton = (<>
    <ReactTooltip place="top" type="dark" effect="solid"/>
    <InactiveReactButton data-tip="Report post" onClick={() => report_post()}>❗</InactiveReactButton>
  </>)
  const unreportButton = (<>
    <ReactTooltip place="top" type="dark" effect="solid"/>
    <ActiveReportButton data-tip="Unreport post" onClick={() => unreport_post()}>❗</ActiveReportButton>
  </>)

  function formatQueue(queue : string) {
    if (!queue.endsWith('queue')) {
      queue += " queue"
    }
    return queue
  }
  let queue = <></>
  if (!(props.accepted || props.deleted || props.reported || props.answered) && props.queue) {
    queue = (<span style={{marginLeft: "10px"}}>
      <ReactTooltip place="top" type="dark" effect="solid"/>
      <Queue data-tip="This indicates which tutor queue your post is currently in">{formatQueue(props.queue)} </Queue>
    </span> )
  }
  
  return (
    <StyledText style={props.type === "comment" ? {paddingTop: "20px"} : props.type === "reply" ? {paddingTop: "10px"}:{}}>
      <StyledPost style={props.type === "reply" ? {paddingLeft: "20px", borderLeft: "2px solid lightgrey"} : (props.type === "comment" ? (props.accepted ? {backgroundColor: "#90EE90", padding: "10px", borderRadius: "10px"} : {}):{})}>
        <OptionsBar>
          <Col>
            {toggleEdit ? <></> : heading}
            <Row>
              {author}{queue}
            </Row>
          </Col>
          <Col>
            <Row>
              {props.private ? <Private>PRIVATE</Private>: <></>}
              {props.anonymous ? <Anonymous>ANONYMOUS</Anonymous>: <></>}
            </Row>
          </Col>
        </OptionsBar>
        
        {props.deleted ? <p style={{color: "darkGrey", fontStyle: "italic", fontWeight: 500}}>{props.text}</p> : <></>}
        <span style={props.deleted ? {display: "none"} : {}}>
          {toggleEdit ? <></> : tags}
          <br/>
          { toggleEdit ? editBox : <p>{props.text}</p> }
          { props.userReacted ? activeReactButton : reactButton}
          { getCurrentUser().user_id === props.author ? ( toggleEdit ? activeEditButton : editButton ) : <></> }
          { toggleReply ? activeReplyButton : replyButton }
          { props.type === "post" && props.showCloseButton ? ( props.closed ? activeCloseButton : closeButton)  : <></> }
          { props.type === "comment" && props.showAcceptButton ? (props.accepted ? activeAcceptButton : acceptButton) : <></> }
          { props.type === "post" && props.showReportButton && !props.reported ? reportButton  : <></> }
          { props.type === "post" && props.showUnreportButton && props.reported ? unreportButton  : <></> }
          { props.type === "post" && props.showDeleteButton ? deleteButton  : <></> }
          { props.type === "comment" && props.showDeleteButton ? deleteCommentButton  : <></> }
          { props.type === "reply" && props.showDeleteButton ? deleteReplyButton  : <></> }
          { toggleReply ? reply : <></>}
        </span>
      
      </StyledPost>
      { props.type === "post" ? <></>: <StyledBorder/>}
    </StyledText>
  );
};

export default TextView;