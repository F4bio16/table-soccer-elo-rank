# Specifiche di interfaccia

## Modelli

### Player

| name | type | description | nullable |
|---|---|---|---|
| id | number | player ID |
| name | string | player name |
| score | number | player rank score | 🗹 |
| rank_position | number | absolute rank position |
| last_results | Array\<boolean\> | results of latest 5 match | 🗹 |
| team | null | not used | 🗹 |

### PlayerScore

| name | type | description | nullable |
|---|---|---|---|
| id | number | player ID |
| name | string | player name |
| score | number | player rank score |
| team | string | not used |
| initial_score | number | user score before the match. -1 if not available |
| earned_score | number | points earned in this match | 🗹 |

### Match


| name | type | description | nullable |
|---|---|---|---|
| id | number | match ID |
| blue_score | number | score of blue team | 🗹 |
| red_score | number | score of red team | 🗹 |
| state | string | state of the match.<br>Expected values:<br> `__initial__`: initial state <br> `__progress__`: match on progress <br>`__suspend__`: match suspended <br>  `__end__`: match ended <br> `__deleted__`: match deleted | |
| blue_players | Array\<PlayerScore\> | Players of blue team | |
| red_players | Array\<PlayerScore\> | Players of red team | |
| start_dt | string | Date rapresentation in ISO string of start of game | |
| end_dt | string | Date rapresentation in ISO string of end of game | 🗹 |
| match_duration | number | duration of the game in seconds | 🗹 |
| args | MatchAttributes | attributes of the game | 🗹 |

### MatchAttributes


| name | type | description | values |
|---|---|---|---|
| blue_humiliated | number | humiliation for blue team | `1` => `true`<br> `0` => `false`
| red_humiliated | number | humiliation for red team | `1` => `true`<br> `0` => `false`

## Lista giocatori

**Method**: `GET`

**Endpoint**: `/api/v1/players/`

### Query parameters:

| name | type | description | mandatory |
|---|---|---|---|
| query | string | filter by 'name' field | no |

### Response

| name | type | description | mandatory |
|---|---|---|---|
| players | Array\<Player\> | list of players | 🗹 |

*Example:*
```json
{
  "players": [
    {
      "id": 13,
      "last_results": [
        true,
        false,
        true,
        true,
        true
      ],
      "name": "Fabio Folchi",
      "rank_position": 1,
      "score": 1135,
      "team": null
    },
    {
      "id": 3,
      "last_results": [
        true,
        false,
        true,
        true
      ],
      "name": "Andrea D'Ippolito",
      "rank_position": 2,
      "score": 1095,
      "team": null
    }
    {
      "id": 26,
      "last_results": [
        true,
        false,
        false,
        true,
        false
      ],
      "name": "Riccardo Bellanova",
      "rank_position": 3,
      "score": 1084,
      "team": null
    }
  ]
}
```

## Lista partite

**Method**: `GET`

**Endpoint**: `/api/v1/matches/`

### Query parameters:

| name | type | description | mandatory |
|---|---|---|---|
| limit | number | max length of returned match<br> *Default: 10* | no |

### Response

| name | type | description | mandatory |
|---|---|---|---|
| matches | Array\<Match\> | list of match | 🗹 |

*Example:*
```json
{
  "matches": [
    {
      "blue_players": [
        {
          "earned_score": 16,
          "id": 28,
          "initial_score": -1,
          "name": "Rosario Brischetto",
          "score": 1116,
          "team": "__blue__"
        },
        {
          "earned_score": 16,
          "id": 3,
          "initial_score": -1,
          "name": "Andrea D'Ippolito",
          "score": 1038,
          "team": "__blue__"
        }
      ],
      "blue_score": 10,
      "id": 29,
      "red_players": [
        {
          "earned_score": -3,
          "id": 11,
          "initial_score": -1,
          "name": "Emiliano Pieri",
          "score": 1042,
          "team": "__red__"
        },
        {
          "earned_score": -3,
          "id": 26,
          "initial_score": -1,
          "name": "Riccardo Bellanova",
          "score": 1084,
          "team": "__red__"
        }
      ],
      "red_score": 7,
      "state": "__end__"
    }
  ]
}

```

## Avvia nuova partita

**Method**: `POST`

**Endpoint**: `/api/v1/matches/start`

### Body request

**ContentType**: `application/json`
| name | type | description | mandatory |
|---|---|---|---|
| red_team | Array<number> | array of Player.id of red team | 🗹 |
| blue_team | Array<number> | array of Player.id of blue team | 🗹 |

*Example:*
```json
{
  "red_team": [1,2],
  "blue_team": [3,4]
}
```

## Body response

| name | type | description | mandatory |
|---|---|---|---|
| game_id | number | game ID | 🗹 |
| expected_scores | ExpectedScore | chance of victory | 🗹 |
| expected_scores.blue_wins | number | percentage of blue victory | 🗹 |
| expected_scores.red_wins | number | percentage of red victory | 🗹 |

*Example:*
```json
{
  "expected_scores": {
    "blue_wins": 0.30265492141014677,
    "red_wins": 0.6973450785898532
  },
  "game_id": 78
}
```

## Completa partita (inserisci risultato)

**Method**: `POST`

**Endpoint**: `/api/v1/matches/{match-id}/complete`

**Query parameter**

| name | type | description | mandatory |
|---|---|---|---|
| match-id | number | match ID | 🗹 |

### Body request

**ContentType**: `application/json`

| name | type | description | mandatory |
|---|---|---|---|
| red_result | number | score result of red team | 🗹 |
| red_humiliated | boolean | true if red team was humiliated. *Default: false* | |
| blue_result | number | score result of red team | 🗹 |
| blue_humiliated | boolean | true if blue team was humiliated. *Default: false* | |

*Example:*
```json
{
  "red_result": 11,
  "red_humiliated": false,
  "blue_result": 5,
  "blue_humiliated": false,
}
```

## Body response

| name | type | description | mandatory |
|---|---|---|---|
| player_scores | Array<Player> | list of players of the match extended with `score_delta` attribute: earned points | 🗹 |

*Example:*
```json
{
  "player_scores": [
    {
      "id": 1,
      "last_results": [
        false,
        false,
        false,
        true,
        false
      ],
      "name": "Fabio",
      "rank_position": null,
      "score": 1094,
      "score_delta": -22,
      "team": "__red__"
    },
    {
      "id": 2,
      "last_results": [
        false,
        false,
        false,
        true,
        false
      ],
      "name": "Riccardo",
      "rank_position": null,
      "score": 1062,
      "score_delta": -22,
      "team": "__red__"
    },
    {
      "id": 3,
      "last_results": [
        false,
        true,
        false,
        false,
        false
      ],
      "name": "Gennaro",
      "rank_position": null,
      "score": 1091,
      "score_delta": 26,
      "team": "__blue__"
    },
    {
      "id": 4,
      "last_results": [
        true,
        true,
        false,
        false,
        false
      ],
      "name": "Saro",
      "rank_position": null,
      "score": 1074,
      "score_delta": 26,
      "team": "__blue__"
    }
  ]
}

```


## Cancella partita

This API call is used to delete a game. A game can be deleted under the following conditions:

- If the game is in the "initial" state.
- If the game is the last game in the "end" state.

**Method**: `DELETE`

**Endpoint**: `/api/v1/matches/{match-id}`

**Query parameter**

| name | type | description | mandatory |
|---|---|---|---|
| match-id | number | match ID | 🗹 |

### Body request

**ContentType**: `text/plain`


## Body response
### Successful Operation

**HTTP Status:** 200

When the operation is successful, the server responds with a status code of 200

### Unsuccessful Operation

When an operation fails, the server responds with an appropriate HTTP status code to indicate the nature of the error. Additionally, the response body contains details regarding the error to assist in troubleshooting.
