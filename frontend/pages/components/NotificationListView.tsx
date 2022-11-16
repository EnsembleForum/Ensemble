import styled from "@emotion/styled";
import React from "react";
import { useSearchParams } from "react-router-dom";
import { Button, Input } from "theme-ui";
import { ApiFetch, getPermission } from "../../App";
import { APIcall, notification, postListItem } from "../../interfaces";
import { theme } from "../../theme";
import AuthorView from "./AuthorView";
import ReactTooltip from 'react-tooltip';
import { StyledButton } from "../GlobalProps";

// Declaring and typing our props
interface Props { }
const StyledLayout = styled.div`
  background-color: ${theme.colors?.muted};
  width: 25vw;
  border-right: 1px solid lightgrey; 
  p {
    margin-left: 10px;
  }
  overflow-y: scroll;
  overflow-x: hidden;
`
const Post = styled.div`
  max-width: 100%;
  height: 50px;
  padding: 10px 20px 25px 20px;
  border-bottom: 1px solid lightgrey;
  &:hover {
    background-color: ${theme.colors?.highlight};
    cursor: pointer;
  }
  * {
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
  }
`

const Heading = styled.div`
  font-weight: 700;
`

// Exporting our example component
const NotificationsListView = (props: Props) => {
  const [notifications, setNotifications] = React.useState<notification[]>();
  let [searchParams, setSearchParams] = useSearchParams();
  React.useEffect(()=>{
    const api: APIcall = {
      method: "GET",
      path: "notifications/list",
    }
    ApiFetch(api)
      .then((data) => {
        const test = data as { notifications: notification[] };
        console.log(test);
        if (test.notifications.length) {
          searchParams.set("notificationId", test.notifications[0].notification_id.toString());
          searchParams.set("postId", test.notifications[0].post.toString());
          searchParams.set("commentId", test.notifications[0].comment ? test.notifications[0].comment.toString(): '');
          searchParams.set("replyId", test.notifications[0].reply ? test.notifications[0].reply.toString() : '');
          setSearchParams(searchParams);
          setNotifications(test.notifications);
        }
      })
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (notifications && notifications.length > 0) {
    return (
      <StyledLayout>
        {
          notifications.map((each) => {
              const styles : any = {}
              if (each.notification_id.toString()===searchParams.get("notificationId")) {
                styles.backgroundColor = theme.colors?.highlight;
              }
              each.post.toString()
              return (
                <Post style={styles}  onClick={() => {
                  searchParams.set("notificationId", each.notification_id.toString());
                  searchParams.set("postId", each.post.toString());
                  searchParams.set("commentId", each.comment ? each.comment.toString() : '');
                  searchParams.set("replyId", each.reply ? each.reply.toString() : '');
                  setSearchParams(searchParams);
                }}>
                  <Heading>{each.heading}</Heading>
                  <div>Body: {each.body}</div>
                </Post>
              );
            }
          ) 
        }
      </StyledLayout>
    );
  }
  return (
    <StyledLayout>
    </StyledLayout>
  )
};

export default NotificationsListView;