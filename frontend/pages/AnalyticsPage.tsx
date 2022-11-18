import styled from "@emotion/styled";
import React from "react";
import { ApiFetch } from "../App";
import { Prettify } from "../global_functions";
import { analytics, APIcall } from "../interfaces";
import AuthorView from "./components/AuthorView";

// Declaring and typing our props
interface Props {}

// Writing styled components
const Layout = styled.div`
  width:100vw;
  height: 80vh;
  display: flex;
  flex-direction: column;
  overflow: auto;
`;
const TotalRow = styled.div`
  width:100vw;
  height: 12vh;
  display: flex;
  align-items: space-evenly;
`;
const RestRow = styled.div`
  width:100vw;
  height: 68vh;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
`;
const Col = styled.div`
  width:70vw;
  height: 60vh;
  padding: 10px;
  display: flex;
  flex-direction: column;
  overflow: auto;
  border: 2px solid lightgrey;
  border-radius: 10px;
  table {
    border-collapse: collapse;
  }
  tr > td {
    text-align: center;
    padding: 0; 
    margin: 0;
    max-width: 30px;
    word-wrap: break-word;
    height: 30px;
    border: 1px solid black;
  }
  tr {
    padding: 20px;
    width: 30px;
    border: 1px solid black;
    min-height: 20px;
  }
`;

const Heading = styled.div`
  margin: 10px;
  font-size: 20px;
  width: 100%;
  text-align: center;
  font-weight: 700;
`

const Total = styled.div`
  width: 33vw;
  height: 20vh;
  margin: 30px;
  display: flex;
  align-content: center;
  justify-content: center;
  font-weight: 300;
  font-size: 30px;
`

// Exporting our example component
const AnalyticsPage = (props: Props) => {
  const [analytics, setAnalytics] = React.useState<analytics>();
  function getAnalytics() {
    const anaCall : APIcall = {
      method: "GET",
      path: "admin/analytics"
    }
    ApiFetch(anaCall).then((data) => {
      const analytics = data as analytics;
      setAnalytics(analytics);
    })
  }
  if (analytics) {
    console.log(analytics);
    return (
      <Layout>
        <TotalRow>
          <Total>Total Posts: {analytics?.total_posts}</Total>
          <Total>Total Comments: {analytics?.total_comments}</Total>
          <Total>Total Replies: {analytics?.total_replies}</Total>
        </TotalRow>
        <RestRow>
          <Col>
            <Heading style={{fontSize: "30px"}}>Top contributors by group</Heading>
            <Heading>All Users</Heading>
            <table>
              { Object.keys(analytics.all_users).map((key) => {
                return (
                  <tr>
                    <td>{Prettify(key)}</td>
                    {analytics.all_users[key].map((entry) => {
                          return (
                            <td><AuthorView userId={entry.user_id}></AuthorView>:  {entry.count.toString()}</td>
                          )
                        })}
                  </tr>
                )
              })}
            </table>

            { analytics.groups.map((entry) => {
                return (
                  <>
                  <Heading>{entry.permission_group_name}</Heading>
                  <table>
                    {Object.keys(entry.stats).map((key) => {
                      return (
                        <tr>
                          <td>{Prettify(key)}</td>
                          {entry.stats[key].map((entry) => {
                            return <td><AuthorView userId={entry.user_id}></AuthorView>:  {entry.count.toString()}</td>
                          })}
                        </tr>
                      )
                    })}
                  </table>
                  </>
                )
              })}
            </Col>
        </RestRow>
      </Layout>
    );
  } else {
    getAnalytics();
    return <Layout style={{padding: "30px"}}>Loading...</Layout>
  }
  
};

export default AnalyticsPage;