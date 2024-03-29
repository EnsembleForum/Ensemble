import styled from "@emotion/styled";
import React from "react";
import { useSearchParams } from "react-router-dom";
import { Input, Textarea } from "theme-ui";
import { ApiFetch, getCurrentUser } from "../../App";
import { APIcall, tag, userView } from "../../interfaces";
import { theme } from "../../theme";
import CommentContext from "../commentContext";
import { StyledButton, Tag } from "../GlobalProps";
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
  showCloseButton?: boolean | null,
  showAcceptButton?: boolean | null,
  showDeleteButton?: boolean | null,
  showReportButton?: boolean | null,
  showUnreportButton?: boolean | null,
  focus?: boolean,
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
const TextView = React.forwardRef((props: Props, customRef: any) => {
  const [inputText, setInputText] = React.useState<string>();
  const [toggleReply, setToggleReply] = React.useState<boolean>(false);
  const [editHeading, setEditHeading] = React.useState<string>(props.heading as string);
  const [editText, setEditText] = React.useState<string>(props.text as string);
  const [toggleEdit, setToggleEdit] = React.useState<boolean>(false);
  const [tags, setTags] = React.useState<tag[]>([]);
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
  async function getTags() {
    const tagCall : APIcall = {
      method: "GET",
      path: "tags/tags_list",
    }
    const tags = await ApiFetch(tagCall) as {tags: tag[]};
    setTags(tags.tags);
  }
  React.useEffect(() => {
    getTags();
  }, [])

  const routes = {
    "post": ["browse/comment/create", "✋ ", "browse/post/react", "post_id", "post_id", "browse/post/edit"],
    "comment": ["browse/reply/create", "👍 ", "browse/comment/react", "comment_id", "comment_id", "browse/comment/edit"],
    "reply": ["browse/reply/create", "👍 ", "browse/reply/react", "comment_id", "reply_id", "browse/reply/edit"],
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
    <span data-tip="Post has been closed by a moderator. Edit post based on feedback to unclose.">🔒{' '}</span>
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


  let tagComponent = <></>;
  if (props.tags) {
    tagComponent = <div style={{marginBottom: "10px"}}>{ tags ? props.tags.map((tag) => {
      const x = tags.find((e) => { return (e.tag_id === tag) });
      if (x !== undefined) {
        return <Tag style={{marginRight: "5px", marginTop: "5px"}}>{x.name}</Tag>
      } 
      return <></>
    }) : <></>}</div>
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
      path: "browse/post/close",
      body: {post_id: props.id}
    }
    await ApiFetch(call);
    setCommentCount(commentCount + 1);
    updatePosts();
  }
  async function answer_post() {
    const call : APIcall = {
      method: "PUT",
      path: "browse/comment/accept",
      body: {comment_id: props.id}
    }
    await ApiFetch(call);
    setCommentCount(commentCount + 1);
    updatePosts();
  }
  async function delete_post() {
    const call : APIcall = {
      method: "DELETE",
      path: "browse/post/delete",
      params: {post_id: props.id.toString()}
    }
    await ApiFetch(call);
    setCommentCount(commentCount + 1);
    updatePosts();
  }
  async function delete_comment() {
    const call : APIcall = {
      method: "DELETE",
      path: "browse/comment/delete",
      params: {comment_id: props.id.toString()}
    }
    await ApiFetch(call);
    setCommentCount(commentCount + 1);
    updatePosts();
  }
  async function delete_reply() {
    const call : APIcall = {
      method: "DELETE",
      path: "browse/reply/delete",
      params: {reply_id: props.id.toString()}
    }
    await ApiFetch(call);
    setCommentCount(commentCount + 1);
    updatePosts();
  }

  async function report_post() {
    const call : APIcall = {
      method: "PUT",
      path: "browse/post/report",
      body: {"post_id": props.id}
    }
    await ApiFetch(call);
    setCommentCount(commentCount + 1);
    updatePosts();
  }
  async function unreport_post() {
    const call : APIcall = {
      method: "PUT",
      path: "browse/post/unreport",
      body: {"post_id": props.id}
    }
    await ApiFetch(call);
    setCommentCount(commentCount + 1);
    updatePosts();
  }
  async function postReply() {
    const usernameCall: APIcall = {
      method: "GET",
      path: "user/profile",
      params: { "user_id": props.author.toString() }
    }
    const user = await ApiFetch(usernameCall) as userView;
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
    if (props.anonymous && inputText?.includes(user.username)) {
      // eslint-disable-next-line no-restricted-globals
      if (confirm("Your comment will reveal the anonymous poster's name. Would you like to continue?")) {
        ApiFetch(call).then(()=>{
          setCommentCount(commentCount + 1);
          setToggleReply(false);
        });
      }
    } else {
      ApiFetch(call).then(()=>{
        setCommentCount(commentCount + 1);
        setToggleReply(false);
      });
    }
  }

  const reply = (
  <StyledReply>
    <Input placeholder="Reply" value={inputText} onChange={(e)=>setInputText(e.target.value)} ></Input>
    <ActiveReactButton onClick={(e) => {postReply()}}>Post</ActiveReactButton>
  </StyledReply>)
  const replyButton = (<><ReactTooltip place="top" type="dark" effect="solid"/><InactiveReactButton data-tip="Reply" onClick={() => setToggleReply(true)}>↩️</InactiveReactButton></>);
  const activeReplyButton = (<ActiveReactButton onClick={() => setToggleReply(false)}>↩️</ActiveReactButton>);
  const editHeadingBox = (<>
    {props.type === "post" ?
      <>
        <Textarea value={editHeading} onChange={(e) => setEditHeading(e.target.value)}></Textarea> 
      </>: <></>
    }</>
  )
  const editBox = (
    <>
      <Textarea style={{marginBottom: "10px"}} value={editText} onChange={(e) => setEditText(e.target.value)}></Textarea>
      <ActiveReactButton onClick={() => {
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
      }}>Save</ActiveReactButton>
    </>
  );
  const editButton = (<>
  <ReactTooltip place="top" type="dark" effect="solid"/>
  <InactiveReactButton data-tip="Edit" onClick={() => setToggleEdit(true)}>✏️</InactiveReactButton>
  </>);
  const activeEditButton = (<InactiveReactButton onClick={() => setToggleEdit(false)}>X</InactiveReactButton>);
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
  const style : {[key: string] : string} = {}
  if (props.type === "comment") style.marginTop = "20px";
  if (props.type === "reply")  style.marginTop = "5px";
  if (props.focus) {
    style.backgroundColor = theme.colors?.highlight as string;
    style.padding = "10px";
    style.borderRadius = "10px";
  }
  const refer = props.focus ? {ref: customRef} : {};
  return (
    <StyledText style={style} {...refer}>
      <StyledPost style={props.type === "reply" ? {paddingLeft: "20px", borderLeft: "2px solid lightgrey"} : (props.type === "comment" ? (props.accepted ? {backgroundColor: "#90EE90", padding: "10px", borderRadius: "10px"} : {}):{})}>
        <OptionsBar>
          <Col>
            {toggleEdit ? <></> : heading}
            <Row>
              {toggleEdit ? <></> :author}{toggleEdit ? <></> :queue}
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
          {
            toggleEdit ? <>
              {editHeadingBox}
              <Row>{author}{queue}</Row>
              {tagComponent}
              {editBox}
              {activeEditButton}
            </> : <>
              {toggleEdit ? <></> : tagComponent}
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
            </> 
          }
        </span>
      
      </StyledPost>
      { props.type === "post" ? <></>: <StyledBorder/>}
    </StyledText>
  );
});

export default TextView;