from datetime import datetime, timedelta
import os
import pandas as pd
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Gestion des EPI - UCAC-ICAM", page_icon="🦺", layout="wide"
)

# Fichier de stockage des données
DB_FILE = "demandes_epi_officiel.csv"

# Dictionnaire des prix unitaires officiels
PRIX_UNITAIRES = {
    "Lunettes (1er choix)": 1500,
    "Lunettes (2eme choix)": 1500,
    "Gants d'électricité (1er choix)": 1500,
    "Gants d'électricité (2eme choix)": 1500,
    "Gants de manutention": 2000,
    "Casque (1er choix)": 5000,
    "Casque (2eme choix)": 3000,
    "Chaussures - BEO WORK": 12000,
    "Chaussures - AMSTRON": 12000,
    "Chaussures - WALKMANDER": 10000,
    "Chaussures - Delta plus": 15000,
    "Multimètre": 20000,
    "Blouse TP chimie": 4000,
}

# Liste des emails administrateurs autorisés
ADMIN_EMAILS = [
    "ninon.ombeandonga@2030.ucac-icam.com",
    "gedidia.mabahou@2030.ucac-icam.com",
]


# GESTION DES SESSIONS EN DIRECT (LIVE ATTENDANCE)
if "live_admins" not in st.session_state:
  st.session_state.live_admins = {}


def nettoyer_et_mettre_a_jour_presence(email):
  now = datetime.now()
  # Mettre à jour l'heure de dernière activité de l'admin actuel
  st.session_state.live_admins[email] = now

  # Supprimer les admins inactifs depuis plus de 5 minutes
  admins_actifs = {}
  for adm, last_seen in st.session_state.live_admins.items():
    if now - last_seen < timedelta(minutes=5):
      admins_actifs[adm] = last_seen
  st.session_state.live_admins = admins_actifs


# Fonction pour charger les données
def charger_donnees():
  if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE, dtype=str, encoding="utf-8-sig")

    if "Payé" in df.columns:
      df["Payé"] = df["Payé"].apply(
          lambda x: True if str(x).strip().lower() in ["payé", "true"] else False
      )
    elif "Statut Paiement" in df.columns:
      df["Payé"] = df["Statut Paiement"].apply(
          lambda x: True if str(x).strip().lower() == "payé" else False
      )
    else:
      df["Payé"] = False

    df["Payé"] = df["Payé"].astype(bool)
    return df
  else:
    colonnes = [
        "Date",
        "Nom",
        "Prénom",
        "Téléphone",
        "Promotion",
        "Résidence",
        "Pointure Chaussures",
        "Payé",
    ] + list(PRIX_UNITAIRES.keys())
    return pd.DataFrame(columns=colonnes)


# Fonction pour sauvegarder les données
def sauvegarder_donnees(df):
  df.to_csv(DB_FILE, index=False, encoding="utf-8-sig")


# --- MENU DE NAVIGATION ---
st.sidebar.title("Navigation 🦺")
menu = st.sidebar.radio(
    "Aller vers",
    [
        "Espace Étudiant (L1 / BP)",
        "Annuler ma commande",
        "Espace Administrateur",
    ],
)

# ==========================================
# REMERCIEMENTS (EN HAUT DE PAGE)
# ==========================================
st.markdown(
    "💡 **Projet collaboratif** — Remerciements particuliers à"
    " **Gedidia-chérubin L2-2030** pour sa contribution à la création de cette"
    " application 🦺"
)
st.divider()

# ==========================================
# 1. ESPACE ÉTUDIANT (Formulaire de recensement)
# ==========================================
if menu == "Espace Étudiant (L1 / BP)":
  st.title("🦺 Fiche de Recensement des EPI - UCAC-ICAM")
  st.markdown(
      "Remplis tes informations personnelles et indique les équipements dont"
      " tu as besoin."
  )

  with st.form("form_epi_officiel"):
    st.subheader("1. Informations Personnelles")
    col1, col2 = st.columns(2)
    with col1:
      nom = st.text_input("Nom *").strip().upper()
      promotion = st.radio("Promotion *", ["L1", "BP"], horizontal=True)
    with col2:
      prenom = st.text_input("Prénom *").strip().capitalize()
      residence = st.radio(
          "Résident(e) *", ["Interne", "Externe"], horizontal=True
      )

    telephone = st.text_input("Numéro de téléphone *").strip()

    st.divider()
    st.subheader("2. Choix des Équipements")
    st.markdown(
        "_Veuillez préciser pour chaque article si vous le voulez ou si vous"
        " l'avez déjà._"
    )

    choix_articles = {}

    st.markdown("### 👓 Lunettes de protection (1 500 F)")
    choix_articles["Lunettes (1er choix)"] = st.radio(
        "Lunettes de protection 1er choix (1500F)",
        ["Je veux", "J'ai déjà"],
        horizontal=True,
        index=None,
    )
    choix_articles["Lunettes (2eme choix)"] = st.radio(
        "Lunettes de protection 2eme choix (1500F)",
        ["Je veux", "J'ai déjà"],
        horizontal=True,
        index=None,
    )

    st.markdown("### ⚡ Gants d'électricité (1 500 F)")
    choix_articles["Gants d'électricité (1er choix)"] = st.radio(
        "Gants d'électricité 1er choix (1500F)",
        ["Je veux", "J'ai déjà"],
        horizontal=True,
        index=None,
    )
    choix_articles["Gants d'électricité (2eme choix)"] = st.radio(
        "Gants d'électricité 2eme choix (1500F)",
        ["Je veux", "J'ai déjà"],
        horizontal=True,
        index=None,
    )

    st.markdown("### 🛠️ Gants de manutention (2 000 F)")
    choix_articles["Gants de manutention"] = st.radio(
        "Gants de manutention (2000F)",
        ["Je veux", "J'ai déjà"],
        horizontal=True,
        index=None,
    )

    st.markdown("### ⛑️ Casque de sécurité")
    choix_articles["Casque (1er choix)"] = st.radio(
        "Casque de sécurité 1er choix (5000F)",
        ["Je veux", "J'ai déjà"],
        horizontal=True,
        index=None,
    )
    choix_articles["Casque (2eme choix)"] = st.radio(
        "Casque de sécurité 2eme choix (3000F)",
        ["Je veux", "J'ai déjà"],
        horizontal=True,
        index=None,
    )

    st.markdown("### 👞 Chaussures de protection")
    choix_articles["Chaussures - BEO WORK"] = st.radio(
        "BEO WORK (12000F)", ["Je veux", "J'ai déjà"], horizontal=True, index=None
    )
    choix_articles["Chaussures - AMSTRON"] = st.radio(
        "AMSTRON (12000F)", ["Je veux", "J'ai déjà"], horizontal=True, index=None
    )
    choix_articles["Chaussures - WALKMANDER"] = st.radio(
        "WALKMANDER (10000F)",
        ["Je veux", "J'ai déjà"],
        horizontal=True,
        index=None,
    )
    choix_articles["Chaussures - Delta plus"] = st.radio(
        "Delta plus (15000F)", ["Je veux", "J'ai déjà"], horizontal=True, index=None
    )

    pointure = st.selectbox(
        "👟 Précisez votre pointure de chaussures (30 à 47) :",
        options=[str(p) for p in range(30, 48)],
        index=11,
    )

    st.markdown("### 🔌 Multimètre & Blouse")
    choix_articles["Multimètre"] = st.radio(
        "MULTIMETRE (20000F)",
        ["Je veux", "J'ai déjà"],
        horizontal=True,
        index=None,
    )
    choix_articles["Blouse TP chimie"] = st.radio(
        "Blouse de TP chimie (4000F)",
        ["Je veux", "J'ai déjà"],
        horizontal=True,
        index=None,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button(
        "Soumettre ma demande", type="primary", use_container_width=True
    )

  if submitted:
    if not nom or not prenom or not telephone:
      st.error(
          "⚠️ Veuillez impérativement remplir votre Nom, Prénom et Numéro de"
          " téléphone."
      )
    else:
      df = charger_donnees()

      montant_total = 0
      articles_demandes = []
      for article, choix in choix_articles.items():
        statut = choix if choix is not None else "Aucun"
        if statut == "Je veux":
          montant_total += PRIX_UNITAIRES[article]
          articles_demandes.append(article)

      if not df.empty:
        existant = (df["Nom"] == nom) & (df["Prénom"] == prenom)
        if existant.any():
          df = df[~existant]
          st.info(
              f"ℹ️ {prenom} {nom}, vos informations précédentes ont été mises"
              " à jour avec succès !"
          )

      nouvelle_demande = {
          "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          "Nom": nom,
          "Prénom": prenom,
          "Téléphone": telephone,
          "Promotion": promotion,
          "Résidence": residence,
          "Pointure Chaussures": pointure,
          "Payé": False,
      }

      for article, choix in choix_articles.items():
        nouvelle_demande[article] = choix if choix is not None else "Aucun"

      df = pd.concat([df, pd.DataFrame([nouvelle_demande])], ignore_index=True)
      sauvegarder_donnees(df)

      st.success(
          f"✅ Merci {prenom} ! Tes informations ont bien été transmises à"
          " l'administration."
      )

      st.markdown("---")
      st.subheader("💳 Récapitulatif de votre commande et Paiement")
      if montant_total > 0:
        st.info(f"💰 **Montant total à régler : {montant_total:,} FCFA**")
        st.write("**Équipements commandés :** " + ", ".join(articles_demandes))

        st.markdown(
            "### 📲 Instructions pour le paiement :\n"
            "Veuillez contacter le **BDE (Bureau Des Étudiants)** pour effectuer"
            " le règlement de vos équipements :\n"
            "- **Destinataire :** Le BDE UCAC-ICAM\n"
            "- **Important :** N'oubliez pas de préciser votre **Nom, Prénom et"
            f" Promotion ({promotion})** lors du paiement."
        )
      else:
        st.success(
            "🎉 Vous avez indiqué posséder déjà tous les équipements ! Aucun"
            " frais à payer."
        )

# ==========================================
# 2. ESPACE ANNULATION DE COMMANDE (Étudiant)
# ==========================================
elif menu == "Annuler ma commande":
  st.title("❌ Annulation de Commande")
  st.markdown(
      "Tu peux annuler ta commande **uniquement si l'argent n'a pas encore été"
      " envoyé** (case non cochée par l'admin)."
  )

  with st.form("form_annulation"):
    nom_annul = st.text_input("Votre Nom *").strip().upper()
    prenom_annul = st.text_input("Votre Prénom *").strip().capitalize()
    tel_annul = st.text_input("Votre Numéro de téléphone *").strip()
    btn_annuler = st.form_submit_button(
        "Demander l'annulation de ma commande", type="secondary"
    )

  if btn_annuler:
    if not nom_annul or not prenom_annul or not tel_annul:
      st.error(
          "⚠️ Veuillez remplir votre Nom, Prénom et Numéro de téléphone pour"
          " identifier votre commande."
      )
    else:
      df = charger_donnees()
      if df.empty:
        st.info("Aucune commande enregistrée.")
      else:
        correspondance = (
            (df["Nom"] == nom_annul)
            & (df["Prénom"] == prenom_annul)
            & (df["Téléphone"] == tel_annul)
        )
        if not correspondance.any():
          st.warning(
              "⚠️ Aucune commande trouvée avec ces informations exactes."
          )
        else:
          est_paye = df.loc[correspondance, "Payé"].values[0]
          if est_paye:
            st.error(
                "❌ Impossible d'annuler : votre paiement a déjà été validé par"
                " l'administration."
            )
          else:
            df = df[~correspondance].reset_index(drop=True)
            sauvegarder_donnees(df)
            st.success(
                f"✅ {prenom_annul} {nom_annul}, votre commande a été annulée"
                " avec succès !"
            )

# ==========================================
# 3. ESPACE ADMINISTRATEUR (Avec suivi Direct)
# ==========================================
elif menu == "Espace Administrateur":
  st.title("🔐 Espace Administrateur - Gestion & Recensement")

  if "admin_connecte" not in st.session_state:
    st.session_state.admin_connecte = False

  if not st.session_state.admin_connecte:
    st.markdown(
        "Veuillez entrer votre adresse email officielle et le mot de passe"
        " administrateur :"
    )
    email_saisi = st.text_input(
        "Email administrateur", placeholder="prenom.nom@2030.ucac-icam.com"
    ).strip().lower()
    mdp_saisi = st.text_input("Mot de passe admin", type="password")

    if st.button("Se connecter", type="primary"):
      if email_saisi in ADMIN_EMAILS and mdp_saisi == "icam":
        st.session_state.admin_connecte = True
        st.session_state.current_admin_email = email_saisi
        st.success("🔓 Connexion réussie !")
        st.rerun()
      else:
        st.error(
            "⛔ Accès refusé. Vérifiez votre email (autorisé) et votre mot de"
            " passe."
        )
  else:
    # Mettre à jour la présence en direct
    nettoyer_et_mettre_a_jour_presence(st.session_state.current_admin_email)

    col_status1, col_status2 = st.columns([3, 1])
    with col_status1:
      st.success(
          f"🔓 Connecté en tant qu'administrateur :"
          f" **{st.session_state.current_admin_email}**"
      )
    with col_status2:
      if st.button("Se déconnecter"):
        if (
            st.session_state.current_admin_email
            in st.session_state.live_admins
        ):
          del st.session_state.live_admins[
              st.session_state.current_admin_email
          ]
        st.session_state.admin_connecte = False
        st.rerun()

    # --- SECTION SESSIONS EN DIRECT ---
    with st.expander("🟢 Administrateurs actuellement connectés en direct"):
      st.write("Voici la liste des administrateurs actifs sur le dashboard :")
      for adm_email, last_seen in st.session_state.live_admins.items():
        st.markdown(
            f"- 🟢 **{adm_email}** *(Dernière activité :"
            f" {last_seen.strftime('%H:%M:%S')})*"
        )

    df = charger_donnees()

    if df.empty:
      st.info("Aucune demande enregistrée pour le moment.")
    else:
      st.info(
          f"📊 Nombre total d'étudiants ayant soumis leur fiche :"
          f" **{len(df)}**"
      )

      df = df.sort_values(by=["Nom", "Prénom"], ascending=[True, True])
      df = df.reset_index(drop=True)

      # ==========================================
      # SECTION A : RECENSEMENT GLOBAL ET BUDGET TOTAL
      # ==========================================
      st.header("📊 1. Recensement global des achats et des coûts")

      recensement_data = []
      grand_total_general = 0

      for article, prix in PRIX_UNITAIRES.items():
        if article in df.columns:
          quantite = (df[article] == "Je veux").sum()
          total_fcfa = quantite * prix
          grand_total_general += total_fcfa
          recensement_data.append({
              "Équipement": article,
              "Prix unitaire": f"{prix:,} F",
              "Quantité à commander": int(quantite),
              "Coût Total": f"{total_fcfa:,} F",
          })

      st.metric(
          label="💰 COÛT TOTAL GÉNÉRAL DE TOUS LES ÉQUIPEMENTS À ACHETER",
          value=f"{grand_total_general:,} FCFA",
      )
      st.markdown("<br>", unsafe_allow_html=True)

      df_recensement = pd.DataFrame(recensement_data)
      st.dataframe(df_recensement, use_container_width=True)

      # ==========================================
      # SECTION CHAUSSURES : MARQUE + POINTURE + PRIX
      # ==========================================
      st.subheader(
          "👟 Détail des chaussures commandées (Marque, Pointure, Prix &"
          " Quantité)"
      )
      chaussures_cols = {
          "Chaussures - BEO WORK": 12000,
          "Chaussures - AMSTRON": 12000,
          "Chaussures - WALKMANDER": 10000,
          "Chaussures - Delta plus": 15000,
      }

      details_chaussures = []
      for col, prix_unit in chaussures_cols.items():
        df_marque = df[df[col] == "Je veux"]
        if not df_marque.empty:
          decompte = df_marque["Pointure Chaussures"].value_counts()
          for pointure, qté in decompte.items():
            cout_total_ligne = int(qté) * prix_unit
            details_chaussures.append({
                "Marque de Chaussure": col.replace("Chaussures - ", ""),
                "Pointure": pointure,
                "Prix unitaire": f"{prix_unit:,} F",
                "Quantité": int(qté),
                "Coût Total": f"{cout_total_ligne:,} F",
            })

      if details_chaussures:
        df_details_chaussures = pd.DataFrame(details_chaussures)
        df_details_chaussures = df_details_chaussures.sort_values(
            by=["Marque de Chaussure", "Pointure"]
        ).reset_index(drop=True)
        st.dataframe(df_details_chaussures, use_container_width=True)
      else:
        st.info("Aucune demande de chaussures pour le moment.")

      st.divider()

      # ==========================================
      # SECTION B : CASES À COCHER & MONTANT DÜ PAR ÉTUDIANT
      # ==========================================
      st.header(
          "📋 2. Validation des Paiements & Montant Dû par Étudiant"
      )
      st.markdown(
          "Cochez la case **Payé** pour valider le règlement d'un étudiant."
      )


      def calculer_montant_et_resume(row):
        total = 0
        manquants = []
        for article, prix in PRIX_UNITAIRES.items():
          if row[article] == "Je veux":
            total += prix
            if "Chaussures" in article:
              manquants.append(f"{article} (Pt {row['Pointure Chaussures']})")
            else:
              manquants.append(article)
        resume = ", ".join(manquants) if manquants else "Rien à commander"
        return pd.Series([f"{total:,} F", resume])


      df[["Montant Dû", "Équipements demandés"]] = df.apply(
          calculer_montant_et_resume, axis=1
      )

      colonnes_a_afficher = [
          "Nom",
          "Prénom",
          "Promotion",
          "Téléphone",
          "Montant Dû",
          "Payé",
          "Équipements demandés",
      ]

      df_edit = st.data_editor(
          df[colonnes_a_afficher],
          use_container_width=True,
          num_rows="fixed",
          key="editeur_paiement_unique",
      )

      if not df_edit.equals(df[colonnes_a_afficher]):
        df["Payé"] = df_edit["Payé"]
        sauvegarder_donnees(df)
        st.success("✅ Statut de paiement mis à jour avec succès !")
        st.rerun()

      st.markdown("<br>", unsafe_allow_html=True)

      # ==========================================
      # SECTION C : SUPPRESSION CIBLÉE D'UN ÉTUDIANT
      # ==========================================
      with st.expander("🗑️ Supprimer un étudiant en particulier"):
        st.markdown(
            "Sélectionnez un étudiant dans la liste pour supprimer"
            " définitivement sa fiche :"
        )
        liste_etudiants = (
            df["Nom"]
            + " "
            + df["Prénom"]
            + " (Tél: "
            + df["Téléphone"]
            + ")"
        ).tolist()

        etudiant_a_supprimer = st.selectbox(
            "Choisissez l'étudiant à supprimer :", options=liste_etudiants
        )

        if st.button(
            "❌ Confirmer la suppression de cet étudiant", type="secondary"
        ):
          index_selectionne = liste_etudiants.index(etudiant_a_supprimer)
          df = df.drop(index_selectionne).reset_index(drop=True)
          sauvegarder_donnees(df)
          st.success(
              f"✅ L'étudiant {etudiant_a_supprimer} a été supprimé avec"
              " succès."
          )
          st.rerun()

      st.markdown("<br>", unsafe_allow_html=True)

      csv = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
      st.download_button(
          label="📥 Télécharger la base de données complète (CSV)",
          data=csv,
          file_name=f"recensement_epi_officiel_{datetime.now().strftime('%Y-%m-%d')}.csv",
          mime="text/csv",
      )

      with st.expander("⚙️ Zone dangereuse"):
        if st.button("🗑️ Effacer toutes les données"):
          if os.path.exists(DB_FILE):
            os.remove(DB_FILE)
            st.rerun()
