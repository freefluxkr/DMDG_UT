import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyAfsuj8YD7_SoFDhxoj45XtxaE6zpjfl40",
  authDomain: "dmdg-ut.firebaseapp.com",
  projectId: "dmdg-ut",
  storageBucket: "dmdg-ut.firebasestorage.app",
  messagingSenderId: "186096508922",
  appId: "1:186096508922:web:6df36008e2ac935aee8e43",
  measurementId: "G-NWBJN2GGQY"
};

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
