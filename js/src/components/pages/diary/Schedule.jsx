import React from 'react';
import {Grid, Typography} from "@material-ui/core";
import {JupyterActivity, ShrimpField, SummaryField, JupyterAllActivities} from "./elements";
import {makeStyles} from "@material-ui/core/styles";
import {Break, ColumnCard, ColumnList, LinkButton, Loading, Text} from "../../elements";
import {setIds} from '../../functions';


const useStyles = makeStyles(theme => ({
    grid: {
        justifyContent: 'flex-start',
        alignItems: 'baseline',
    },
}));


export default function Schedule(props) {

    const {json, history} = props;

    if (json === null) {
        return <Loading/>;  // undefined initial data
    } else {
        setIds(json);
        // drop outer date label since we already have that in the page
        return (<ColumnList>
            {json.slice(1).map(row => <TopLevelPaper json={row} history={history} key={row.id}/>)}
        </ColumnList>);
    }
}


function childrenFromRest(head, rest, level, history) {
    let children = [];
    rest.forEach((row) => {
        if (Array.isArray(row)) {
            if (head === 'shrimp') {
                children.push(<ShrimpField json={row} key={row.id}/>);
            } else {
                children.push(<Break/>);
                children.push(<Header json={row} level={level} history={history} key={row.id}/>);
            }
        } else {
            children.push(<Field json={row} key={row.id}/>);
        }
    });
    return children;
}


function TopLevelPaper(props) {
    const {json, history} = props;
    const [head, ...rest] = json;
    const children = childrenFromRest(head.tag, rest,3, history);
    return (<ColumnCard header={head.value}>{children}</ColumnCard>);
}


function Header(props) {

    const {json, level, history} = props;
    const [head, ...rest] = json;
    const classes = useStyles();

    const children = head.tag === 'jupyter-activity' ?
        <JupyterActivity json={rest}/> :
        childrenFromRest(head.tag, rest, level + 1, history);

    return (<>
        <Grid item xs={4} className={classes.grid}>
            <Typography variant={'h' + level}>{head.value}</Typography>
        </Grid>
        {children}
    </>);
}


function Field(props) {

    const {json} = props;

    if (json.type === 'value') {
        return <SummaryField json={json}/>
    } else if (json.type === 'link') {
        if (json.tag === 'health') {
            return <LinkButton href='api/jupyter/health'><Text>{json.value}</Text></LinkButton>
        } else if (json.tag === 'all-activities') {
            return <JupyterAllActivities json={json}/>
        } else {
            return (<Grid item xs={4}><Text>Unsupported link: {JSON.stringify(json)}</Text></Grid>);
        }
    } else {
        return (<Grid item xs={4}><Text>Unsupported type: {JSON.stringify(json)}</Text></Grid>);
    }
}
