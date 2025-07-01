#add slots - randint 
streamlit as st
import random
import time

# ───── Initialization ─────
if "screen" not in st.session_state:
    st.session_state.screen = "home"
if "balance" not in st.session_state:
    st.session_state.balance = 100
if "stats" not in st.session_state:
    st.session_state.stats = {
        "dice": {"wins": 0, "losses": 0},
        "roulette": {"wins": 0, "losses": 0},
        "wheel": {"wins": 0, "losses": 0},
        "blackjack": {"wins": 0, "losses": 0}
    }

# ───── Helper Functions ─────
def deal_card():
    return random.randint(1, 11)

def calculate_score(cards):
    score = sum(cards)
    if 11 in cards and score > 21:
        score -= 10
    return score

def show_header(title):
    col1, col2 = st.columns([4, 1])
    with col1:
        st.subheader(title)
    with col2:
        st.markdown(f"### 💰 €{st.session_state.balance}")

# ───── Game Functions ─────
def dice_duel():
    show_header("🎲 Dice Duel")
    if st.button("Roll Dice"):
        placeholder = st.empty()
        for _ in range(5):
            placeholder.markdown(f"🎲 Rolling... {random.randint(1, 6)} vs {random.randint(1, 6)}")
            time.sleep(0.3)
        player = random.randint(1, 6)
        computer = random.randint(1, 6)
        placeholder.markdown(f"🎲 You rolled: {player} | Computer rolled: {computer}")
        if player > computer:
            st.success("You win!")
            st.session_state.balance += 10
            st.session_state.stats["dice"]["wins"] += 1
        elif player < computer:
            st.error("You lose!")
            st.session_state.balance -= 10
            st.session_state.stats["dice"]["losses"] += 1
        else:
            st.info("It's a tie!")
    if st.button("🔙 Back to Menu"):
        st.session_state.screen = "home"
        st.rerun()

def roulette():
    show_header("🎯 Roulette")
    bet = st.number_input("Place your bet", min_value=1, max_value=st.session_state.balance, value=10)
    choice = st.selectbox("Choose color", ["Red", "Black"])
    if st.button("Spin"):
        placeholder = st.empty()
        for _ in range(10):
            placeholder.markdown(f"🎡 Spinning... {random.choice(['Red', 'Black', 'Green'])}")
            time.sleep(0.2)
        result = random.choice(["Red", "Black", "Green"])
        placeholder.markdown(f"🎯 The ball landed on: **{result}**")
        if result == choice:
            st.success("You win!")
            st.session_state.balance += bet
            st.session_state.stats["roulette"]["wins"] += 1
        else:
            st.error("You lose!")
            st.session_state.balance -= bet
            st.session_state.stats["roulette"]["losses"] += 1
    if st.button("🔙 Back to Menu"):
        st.session_state.screen = "home"
        st.rerun()

def wheel_of_fortune():
    show_header("🎡 Wheel of Fortune")
    if st.button("Spin the Wheel"):
        placeholder = st.empty()
        outcomes = ["Win 50", "Lose 20", "Win 10", "Lose 10", "Bankrupt", "Double Balance"]
        for _ in range(10):
            placeholder.markdown(f"🎡 {random.choice(outcomes)}")
            time.sleep(0.2)
        outcome = random.choice(outcomes)
        placeholder.markdown(f"🎉 Result: **{outcome}**")
        if outcome == "Win 50":
            st.session_state.balance += 50
            st.session_state.stats["wheel"]["wins"] += 1
        elif outcome == "Lose 20":
            st.session_state.balance -= 20
            st.session_state.stats["wheel"]["losses"] += 1
        elif outcome == "Win 10":
            st.session_state.balance += 10
            st.session_state.stats["wheel"]["wins"] += 1
        elif outcome == "Lose 10":
            st.session_state.balance -= 10
            st.session_state.stats["wheel"]["losses"] += 1
        elif outcome == "Bankrupt":
            st.session_state.balance = 0
            st.session_state.stats["wheel"]["losses"] += 1
        elif outcome == "Double Balance":
            st.session_state.balance *= 2
            st.session_state.stats["wheel"]["wins"] += 1
    if st.button("🔙 Back to Menu"):
        st.session_state.screen = "home"
        st.rerun()

def view_stats():
    show_header("📊 Game Stats")
    for game, data in st.session_state.stats.items():
        st.write(f"**{game.capitalize()}** - Wins: {data['wins']}, Losses: {data['losses']}")
    if st.button("🔙 Back to Menu"):
        st.session_state.screen = "home"
        st.rerun()

def blackjack():
    show_header("🃏 Blackjack")
    if "bj_player" not in st.session_state:
        st.session_state.bj_player = []
        st.session_state.bj_dealer = []
        st.session_state.bj_over = False

    if st.session_state.bj_player == []:
        bet = st.number_input("Place your bet", min_value=1, max_value=st.session_state.balance, value=10)
        if st.button("Start Game"):
            st.session_state.bj_bet = bet
            st.session_state.balance -= bet
            st.session_state.bj_player = [deal_card(), deal_card()]
            st.session_state.bj_dealer = [deal_card(), deal_card()]
            st.session_state.bj_over = False
        else:
            return

    p = st.session_state.bj_player
    d = st.session_state.bj_dealer
    st.write(f"Your cards: {p} | Total: {calculate_score(p)}")
    st.write(f"Dealer shows: {d[0]}")

    if not st.session_state.bj_over:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Hit"):
                p.append(deal_card())
                if calculate_score(p) > 21:
                    st.session_state.bj_over = True
        with col2:
            if st.button("Stand"):
                while calculate_score(d) < 17:
                    d.append(deal_card())
                st.session_state.bj_over = True

    if st.session_state.bj_over:
        st.write(f"Dealer's cards: {d} | Total: {calculate_score(d)}")
        player_score = calculate_score(p)
        dealer_score = calculate_score(d)
        if player_score > 21:
            st.error("You busted! Dealer wins.")
            st.session_state.stats["blackjack"]["losses"] += 1
        elif dealer_score > 21 or player_score > dealer_score:
            st.success("You win!")
            st.session_state.balance += st.session_state.bj_bet * 2
            st.session_state.stats["blackjack"]["wins"] += 1
        elif player_score == dealer_score:
            st.info("It's a draw.")
            st.session_state.balance += st.session_state.bj_bet
        else:
            st.error("Dealer wins.")
            st.session_state.stats["blackjack"]["losses"] += 1

        if st.button("🔙 Back to Menu"):
            st.session_state.screen = "home"
            st.session_state.bj_player = []
            st.session_state.bj_dealer = []
            st.rerun()

# ───── Main Menu ─────
def main_menu():
    show_header("🎰 Casino Game Hub")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎲 Dice Duel"):
            st.session_state.screen = "dice"
            st.rerun()
        if st.button("🃏 Blackjack"):
            st.session_state.screen = "blackjack"
            st.rerun()
    with col2:
        if st.button("🎯 Roulette"):
            st.session_state.screen = "roulette"
            st.rerun()
        if st.button("🎡 Wheel of Fortune"):
            st.session_state.screen = "wheel"
            st.rerun()

    st.markdown("---")
    if st.button("📊 View Stats"):
        st.session_state.screen = "stats"
        st.rerun()
    if st.button("🔄 Reset Game"):
        st.session_state.balance = 100
        for game in st.session_state.stats:
            for k in st.session_state.stats[game]:
                st.session_state.stats[game][k] = 0
        st.success("Game reset!")

# ───── Routing ─────
if st.session_state.screen == "home":
    main_menu()
elif st.session_state.screen == "dice":
    dice_duel()
elif st.session_state.screen == "roulette":
    roulette()
elif st.session_state.screen == "wheel":
    wheel_of_fortune()
elif st.session_state.screen == "stats":
    view_stats()
elif st.session_state.screen == "blackjack":
    blackjack()
