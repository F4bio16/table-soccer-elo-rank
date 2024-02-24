const endpoint = window.location.origin + "/api/v1"

let red_team = [0,0]
let blue_team = [0,0]
let red_players_current = [0,0]
let blue_players_current = [0,0]

let all_players = []

function sortByRank(a, b) {
    return a.score - b.score;
}

function rematch(rematch_button){
    let tr = $(rematch_button).parents('tr')
    let b1 = $(tr).find('.blue_team').first().attr('data-id') + ' - ' + $(tr).find('.blue_team').first().text()
    let b2 = $(tr).find('.blue_team').last().attr('data-id') + ' - ' + $(tr).find('.blue_team').last().text()
    let r1 = $(tr).find('.red_team').first().attr('data-id') + ' - ' + $(tr).find('.red_team').first().text()
    let r2 = $(tr).find('.red_team').last().attr('data-id') + ' - ' + $(tr).find('.red_team').last().text()
    location.href = '/index.html?b1='+b1+'&b2='+b2+'&r1='+r1+'&r2='+r2
}

function fillForRematch(){
    const searchParams = new URLSearchParams(window.location.search);

    // Iterating the search parameters
    for (const p of searchParams) {
        if(p[0]=='b1'){
            let selection = p[1]
            autoCompleteJSB1.input.value = selection;
            blue_team[0] = parseInt(selection.split(' - ')[0])
            blue_players_current[0] = selection.split(' - ')[1]
        }
        if(p[0]=='b2'){
            let selection = p[1]
            autoCompleteJSB2.input.value = selection;
            blue_team[1] = parseInt(selection.split(' - ')[0])
            blue_players_current[1] = selection.split(' - ')[1]
        }
        if(p[0]=='r1'){
            let selection = p[1]
            autoCompleteJSR1.input.value = selection;
            red_team[0] = parseInt(selection.split(' - ')[0])
            red_players_current[0] = selection.split(' - ')[1]
        }
        if(p[0]=='r2'){
            let selection = p[1]
            autoCompleteJSR2.input.value = selection;
            red_team[1] = parseInt(selection.split(' - ')[0])
            red_players_current[1] = selection.split(' - ')[1]
        }
    }
}

function deleteMatch(matchId){
    $.ajax({
        type: "DELETE",
        contentType: "application/json",
        url: endpoint + "/matches/"+ matchId,
        data: JSON.stringify({}),
        success: function(data) {
            let match_id_tr = $('tr').find(`[data-match-id='${matchId}']`)
            $(match_id_tr).remove()
        }
    })
}

function updateLatest(){
    $.ajax({
        type: "GET",
        contentType: "application/json",
        url: endpoint + "/matches/?limit=100",
        success: function(data) {
            $all_table = $('#all_matches')
            $all_table.html('')
            let filterd_matches = data['matches'].filter((match) => match.state != '__deleted__');
            $.each(filterd_matches, function( index, value ) {
            function drawPlayerRow (team, player) {
                const playerNameClass = team === 'blue' ? 'blue_team bg-primary' : 'red_team bg-danger'
                const earnedScore = player.earned_score === null ? '--' : player.earned_score > 0 ? `+ ${player.earned_score}` : player.earned_score
                const earnedScoreColor = player.earned_score > 0 ? 'green' : 'red'

                row += `<div class="row p-1">
                        <span class='col-12 col-lg-6 badge ${playerNameClass}' data-id="`+player.id+`">${player.name}</span>
                        <span class="col-12 col-lg-6">
                            ${player.initial_score !== -1 ? player.initial_score : 'n/a'} <b style="color: ${earnedScoreColor}">(${earnedScore})</b>
                        </span>
                        </div>`
            }

            let blue_score_colored = "<button type='button' class='btn btn-success position-relative'>"+value['blue_score']+"</button>"
            if(value['args']['blue_humiliated'] == 1){
                blue_score_colored = "<button type='button' class='btn btn-success position-relative'>\
                "+ value['blue_score'] +"\
                <span class='position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger'>\
                <i class='fa-solid fa-person-praying'></i></i>\
                </span></button>"
            }
            if(value['blue_score'] < value['red_score']){
                blue_score_colored = "<button type='button' class='btn btn-secondary position-relative'>"+value['blue_score']+"</button>"
                if(value['args']['blue_humiliated'] == 1){
                    blue_score_colored = "<button type='button' class='btn btn-secondary position-relative'>\
                    "+ value['blue_score'] +"\
                    <span class='position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger'>\
                    <i class='fa-solid fa-person-praying'></i></i>\
                    </span></button>"
                }
            }

            let red_score_colored = "<button type='button' class='btn btn-success position-relative'>"+value['red_score']+"</button>"
            if(value['args']['red_humiliated'] == 1){
                red_score_colored = "<button type='button' class='btn btn-success position-relative'>\
                "+ value['red_score'] +"\
                <span class='position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger'>\
                <i class='fa-solid fa-person-praying'></i></i>\
                </span></button>"
            }
            if(value['red_score'] < value['blue_score']){
                red_score_colored = "<button type='button' class='btn btn-secondary position-relative'>"+value['red_score']+"</button>"
                if(value['args']['red_humiliated'] == 1){
                    red_score_colored = "<button type='button' class='btn btn-secondary position-relative'>\
                    "+ value['red_score'] +"\
                    <span class='position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger'>\
                    <i class='fa-solid fa-person-praying'></i></i>\
                    </span></button>"
                }
            }

            let row = `<tr class='match_row' data-match-id=${value['id']}><td class='center'>${value['id']}`
            if(value['state'] != '__initial__'){
                row = row + `<br><button class='rematch_button btn bg-warning'><i class="fa-solid fa-arrows-rotate"></i></button>`
            }
            
            if(value['state'] == '__initial__' || value['id'] == filterd_matches[0]['id'] ){
                row = row + `<span class="delete_match"><br><button class='btn delete_match bg-light'><i class='fa-regular fa-trash-can'></i></button></span>`
            }
            row = row + `</td>`

            row += '<td class="center"><table class="center" style="width: 100%;"><tbody>'
            value.blue_players.forEach(drawPlayerRow.bind(this, 'blue'))
            row += '</tbody> </table> </td>'

            if(value['state'] == "__end__"){
                row = row + "<td style='text-align:right'>"+blue_score_colored+"</td><td style='text-align:left'>"+red_score_colored+"</td>"
            } else {
                row = row + "<td colspan='2' class='center'><button class='btn btn-warning btn-sm add_match_result'>Inserisci risultato</button></td>"
            }

            row += '<td class="center"><table class="center" style="width: 100%;"><tbody>'
            value.red_players.forEach(drawPlayerRow.bind(this, 'red'))
            row += '</tbody> </table> </td>'

            $all_table.append(row)
            });
        }
    });
}

const autoCompleteJSB1 = new autoComplete({
    placeHolder: "Cerca giocatore 1...",
    selector: "#autoCompleteB1",
    data: {
        src: all_players,
        cache: true,
    },
    resultItem: {
        highlight: true
    },
    events: {
        input: {
            selection: (event) => {
                const selection = event.detail.selection.value;
                autoCompleteJSB1.input.value = selection;
                blue_team[0] = parseInt(selection.split(' - ')[0])
                blue_players_current[0] = selection.split(' - ')[1]
            }
        }
    }
});

const autoCompleteJSB2 = new autoComplete({
    placeHolder: "Cerca giocatore 2...",
    selector: "#autoCompleteB2",
    data: {
        src: all_players,
        cache: true,
    },
    resultItem: {
        highlight: true
    },
    events: {
        input: {
            selection: (event) => {
                const selection = event.detail.selection.value;
                autoCompleteJSB2.input.value = selection;
                blue_team[1] = parseInt(selection.split(' - ')[0])
                blue_players_current[1] = selection.split(' - ')[1]
            }
        }
    }
});

const autoCompleteJSR1 = new autoComplete({
    placeHolder: "Cerca giocatore 1...",
    selector: "#autoCompleteR1",
    data: {
        src: all_players,
        cache: true,
    },
    resultItem: {
        highlight: true
    },
    events: {
        input: {
            selection: (event) => {
                const selection = event.detail.selection.value;
                autoCompleteJSR1.input.value = selection;
                red_team[0] = parseInt(selection.split(' - ')[0])
                red_players_current[0] = selection.split(' - ')[1]
            }
        }
    }
});

const autoCompleteJSR2 = new autoComplete({
    placeHolder: "Cerca giocatore 2...",
    selector: "#autoCompleteR2",
    data: {
        src: all_players,
        cache: true,
    },
    resultItem: {
        highlight: true
    },
    events: {
        input: {
            selection: (event) => {
                const selection = event.detail.selection.value;
                autoCompleteJSR2.input.value = selection;
                red_team[1] = parseInt(selection.split(' - ')[0])
                red_players_current[1] = selection.split(' - ')[1]
            }
        }
    }
});





$(document).ready(function(){
    
    updateLatest();
    fillForRematch()
    
    $.ajax({
      type: "GET",
      url: endpoint + "/players/",
      contentType: "application/json",
      success: function(data) {
        $.each(data.players, function( index, value ) {
          all_players.push(value['id'] + ' - '+value['name'])
        })
      }
    })

  })