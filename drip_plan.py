"""
Drip Feed Plan — Custom 5-day schedule for the ML Algorithms from Scratch project.
Covers May 5-9, 2026.
"""

DRIP_PLAN_ML_PORTFOLIO = [
    # Day 1 — Foundation: Linear Regression + Decision Tree
    (
        "Add Linear Regression and Decision Tree implementations with datasets",
        [
            ".gitignore",
            "price.csv",
            "Book2.csv",
            "master_decision.csv",
            "Linear Regression/1.py",
            "Linear Regression/2.py",
            "Linear Regression/linear_regression_streamlit.py",
            "Linear Regression/multiple_linear_regression_streamlit.py",
            "Linear Regression/price.csv",
            "Linear Regression/Book2.csv",
            "Desicion Tree/Master's decision.py",
            "Desicion Tree/Pet_Type.py",
            "Desicion Tree/Shirt_Size.py",
            "Desicion Tree/Transport_mode.py",
            "Desicion Tree/Streamlit.py",
            "Desicion Tree/master_decision.csv",
            "Desicion Tree/pet_type.csv",
            "Desicion Tree/shirt_size.csv",
            "Desicion Tree/transport_mode.csv",
            "Desicion Tree/price.csv",
            "Desicion Tree/Book2.csv",
        ]
    ),

    # Day 2 — Ensemble + KNN + K-Means
    (
        "Implement Random Forest, KNN, and K-Means clustering algorithms",
        [
            "Random forest/1.py",
            "Random forest/2.py",
            "Random forest/3.py",
            "Random forest/4.py",
            "Random forest/5.py",
            "Random forest/6.py",
            "Random forest/mini_project.py",
            "Random forest/master_decision.csv",
            "Random forest/pet_type.csv",
            "Random forest/shirt_size.csv",
            "Random forest/transport_mode.csv",
            "Random forest/data - data.csv.csv",
            "knn/1.py",
            "knn/1_streamlit.py",
            "knn/improved_moviedataset.csv",
            "knn/high_accuracy_moviedataset.csv",
            "k-means/1.py",
            "k-means/streamlit1.py",
            "k-means/mall_customers.csv",
            "mall_customers.csv",
            "improved_moviedataset.csv",
        ]
    ),

    # Day 3 — NLP + Sentiment Analysis + Cosine Similarity
    (
        "Add NLP pipelines, Sentiment Analysis, and Cosine Similarity modules",
        [
            "NLP/1.py",
            "NLP/text_generator.py",
            "NLP/sentiment analysis.csv",
            "NLP/ngram.csv",
            "sentiment_analysis/with_sckit_learn.py",
            "sentiment_analysis/without_libraray.py",
            "sentiment_analysis/withvadersentiment.py",
            "cosine_similarity/app.py",
            "cosine_similarity/app1.py",
            "cosine_similarity/cosine.py",
            "cosine_similarity/project.py",
            "cosine_similarity/similarity.py",
        ]
    ),

    # Day 4 — Deep Learning + LLM + Computer Vision
    (
        "Add TensorFlow LSTM, BERT embeddings, LLM chatbot, and MediaPipe hand tracking",
        [
            "deep_learning/bert.py",
            "deep_learning/tensor_flow.py",
            "deep_learning/whatsapp.csv",
            "LLM/basic.py",
            "LLM/chatbot.py",
            "LLM/simi.py",
            "AI_doddle.py",
            "MI_algorithms_suite.py",
            "improved_MI_algorithms_suite.py",
        ]
    ),

    # Day 5 — Session projects + Streamlit apps + search tools
    (
        "Add Streamlit session apps, search tools, and data science projects",
        [
            "session/1.py",
            "session/Expense tracker.py",
            "session/Login_page.py",
            "session/api.py",
            "session/bank.py",
            "session/dashboard.py",
            "session/game.py",
            "session/role.py",
            "session/signup.py",
            "session/spotify.py",
            "session/streamlit_style.py",
            "session/student_management_system.py",
            "session/uber.py",
            "session/sales.csv",
            "session/spotify.csv",
            "session/uber.csv",
            "session/user.csv",
            "session/users.csv",
            "search/dynamic_map.py",
            "search/dynamic_search.py",
            "search/travel_finder.py",
            "Datascience_project/app.py",
            "Datascience_project/1.py",
            "Datascience_project/2.py",
            "Datascience_project/3.py",
            "Datascience_project/4.py",
            "Datascience_project/data_bot.py",
            "Datascience_project/test.py",
            "Datascience_project/users.csv",
        ]
    ),
]



DRIP_PLAN_15_DAYS = [
    (
        "Linear Algebra (Matrix multiplication, eigenvectors)",
        [
            "Cheat_Sheet.md",
            "Day_01_math_fundamentals/linear_algebra.py",
            "Day_01_math_fundamentals/matrix_ops.py",
            "Day_01_math_fundamentals/eigen_solver.py"
        ]
    ),
    (
        "Calculus (Derivatives, chain rule for backprop)",
        [
            "Day_02_calculus/derivatives.py",
            "Day_02_calculus/chain_rule.py",
            "Day_02_calculus/partial_derivatives.py"
        ]
    ),
    (
        "Forward Propagation (Passing data through neurons)",
        [
            "Day_03_forward_prop/neuron.py",
            "Day_03_forward_prop/activation_functions.py",
            "Day_03_forward_prop/dense_layer.py"
        ]
    ),
    (
        "Loss Functions (MSE, Cross-Entropy)",
        [
            "Day_04_loss_functions/mse.py",
            "Day_04_loss_functions/cross_entropy.py",
            "Day_04_loss_functions/hinge_loss.py"
        ]
    ),
    (
        "Gradient Descent & Backpropagation",
        [
            "Day_05_backprop/gradient_descent.py",
            "Day_05_backprop/backpropagation.py",
            "Day_05_backprop/optimizer_adam.py"
        ]
    ),
    (
        "OpenCV basics (Edge detection, blurring)",
        [
            "Day_06_opencv_filters/edge_detect.py",
            "Day_06_opencv_filters/blur_gaussian.py",
            "Day_06_opencv_filters/color_spaces.py"
        ]
    ),
    (
        "Convolutions (Building CNN filters from scratch)",
        [
            "Day_07_convolutions/conv2d.py",
            "Day_07_convolutions/padding.py",
            "Day_07_convolutions/stride_math.py"
        ]
    ),
    (
        "Pooling Layers (Max pooling, Average pooling)",
        [
            "Day_08_pooling/max_pool.py",
            "Day_08_pooling/avg_pool.py",
            "Day_08_pooling/global_pool.py"
        ]
    ),
    (
        "Complete CNN Architecture",
        [
            "Day_09_cnn_architecture/vgg_style.py",
            "Day_09_cnn_architecture/resnet_block.py",
            "Day_09_cnn_architecture/model_summary.py"
        ]
    ),
    (
        "Regularization (Dropout, Early Stopping)",
        [
            "Day_10_regularization/dropout.py",
            "Day_10_regularization/l2_penalty.py",
            "Day_10_regularization/early_stopping.py"
        ]
    ),
    (
        "Tokenization & Bag of Words",
        [
            "Day_11_nlp_basics/tokenizer.py",
            "Day_11_nlp_basics/bag_of_words.py",
            "Day_11_nlp_basics/stop_words.py"
        ]
    ),
    (
        "TF-IDF & Word Embeddings",
        [
            "Day_12_embeddings/tf_idf.py",
            "Day_12_embeddings/word2vec_sim.py",
            "Day_12_embeddings/cosine_distance.py"
        ]
    ),
    (
        "RNNs & LSTMs",
        [
            "Day_13_recurrent_nets/rnn_cell.py",
            "Day_13_recurrent_nets/lstm_gate.py",
            "Day_13_recurrent_nets/gru_math.py"
        ]
    ),
    (
        "Self-Attention Mechanism",
        [
            "Day_14_attention/self_attention.py",
            "Day_14_attention/multi_head.py",
            "Day_14_attention/scaled_dot_product.py"
        ]
    ),
    (
        "Transformer Block Architecture",
        [
            "Day_15_transformers/encoder_block.py",
            "Day_15_transformers/decoder_block.py",
            "Day_15_transformers/positional_encoding.py"
        ]
    ),
]


DRIP_PLAN_ML_PORTFOLIO = [
    (
        "Add Linear Regression and Decision Tree implementations with datasets",
        [
            ".gitignore", "price.csv", "Book2.csv", "master_decision.csv",
            "Linear Regression/1.py", "Linear Regression/2.py",
            "Linear Regression/linear_regression_streamlit.py",
            "Linear Regression/multiple_linear_regression_streamlit.py",
            "Linear Regression/price.csv", "Linear Regression/Book2.csv",
            "Desicion Tree/Master's decision.py", "Desicion Tree/Pet_Type.py",
            "Desicion Tree/Shirt_Size.py", "Desicion Tree/Transport_mode.py",
            "Desicion Tree/Streamlit.py", "Desicion Tree/master_decision.csv",
            "Desicion Tree/pet_type.csv", "Desicion Tree/shirt_size.csv",
            "Desicion Tree/transport_mode.csv", "Desicion Tree/price.csv",
            "Desicion Tree/Book2.csv",
        ]
    ),
    (
        "Implement Random Forest, KNN, and K-Means clustering algorithms",
        [
            "Random forest/1.py", "Random forest/2.py", "Random forest/3.py",
            "Random forest/4.py", "Random forest/5.py", "Random forest/6.py",
            "Random forest/mini_project.py", "Random forest/master_decision.csv",
            "Random forest/pet_type.csv", "Random forest/shirt_size.csv",
            "Random forest/transport_mode.csv", "Random forest/data - data.csv.csv",
            "knn/1.py", "knn/1_streamlit.py", "knn/improved_moviedataset.csv",
            "knn/high_accuracy_moviedataset.csv", "k-means/1.py",
            "k-means/streamlit1.py", "k-means/mall_customers.csv",
            "mall_customers.csv", "improved_moviedataset.csv",
        ]
    ),
    (
        "Add NLP pipelines, Sentiment Analysis, and Cosine Similarity modules",
        [
            "NLP/1.py", "NLP/text_generator.py", "NLP/sentiment analysis.csv",
            "NLP/ngram.csv", "sentiment_analysis/with_sckit_learn.py",
            "sentiment_analysis/without_libraray.py", "sentiment_analysis/withvadersentiment.py",
            "cosine_similarity/app.py", "cosine_similarity/app1.py",
            "cosine_similarity/cosine.py", "cosine_similarity/project.py",
            "cosine_similarity/similarity.py",
        ]
    ),
    (
        "Add TensorFlow LSTM, BERT embeddings, LLM chatbot, and MediaPipe hand tracking",
        [
            "deep_learning/bert.py", "deep_learning/tensor_flow.py",
            "deep_learning/whatsapp.csv", "LLM/basic.py", "LLM/chatbot.py",
            "LLM/simi.py", "AI_doddle.py", "MI_algorithms_suite.py",
            "improved_MI_algorithms_suite.py",
        ]
    ),
    (
        "Add Streamlit session apps, search tools, and data science projects",
        [
            "session/1.py", "session/Expense tracker.py", "session/Login_page.py",
            "session/api.py", "session/bank.py", "session/dashboard.py",
            "session/game.py", "session/role.py", "session/signup.py",
            "session/spotify.py", "session/streamlit_style.py",
            "session/student_management_system.py", "session/uber.py",
            "session/sales.csv", "session/spotify.csv", "session/uber.csv",
            "session/user.csv", "session/users.csv", "search/dynamic_map.py",
            "search/dynamic_search.py", "search/travel_finder.py",
            "Datascience_project/app.py", "Datascience_project/1.py",
            "Datascience_project/2.py", "Datascience_project/3.py",
            "Datascience_project/4.py", "Datascience_project/data_bot.py",
            "Datascience_project/test.py", "Datascience_project/users.csv",
        ]
    )
]


DRIP_PLAN_AGENTIC_AI = [
    # Day 1 (June 27 - ALREADY DONE)
    (
        "Initialize project with ReAct agent and conversational memory",
        [
            ".gitignore",
            "01_Basic_ReAct_Agent\\react_agent.py",
            "02_Conversational_Memory\\memory_agent.py",
        ]
    ),
    # Day 2 (June 28 - ALREADY DONE)
    (
        "Add custom tool calling and web research agents",
        [
            "03_Custom_Tool_Calling\\custom_tools.py",
            "04_Web_Research_Agent\\web_agent.py",
        ]
    ),
    # Day 3
    (
        "Implement SQL database agent with natural language querying",
        ["05_SQL_Database_Agent\\sql_agent.py"]
    ),
    # Day 4
    (
        "Build document QA system with basic RAG pipeline",
        ["06_Document_QA_Basic_RAG\\rag_agent.py"]
    ),
    # Day 5
    (
        "Add advanced hybrid search with dense and sparse retrieval",
        ["07_Advanced_RAG_Hybrid_Search\\hybrid_search.py"]
    ),
    # Day 6
    (
        "Implement self-reflective critic agent with iterative refinement",
        ["08_Self_Reflective_Agent\\critic_agent.py"]
    ),
    # Day 7
    (
        "Build LangGraph state machine for stateful agent workflows",
        ["09_LangGraph_Basics\\state_machine.py"]
    ),
    # Day 8
    (
        "Add human-in-the-loop approval gates to LangGraph pipelines",
        ["10_LangGraph_Human_in_Loop\\human_approval.py"]
    ),
    # Day 9
    (
        "Implement multi-agent supervisor orchestration pattern",
        ["11_Multi_Agent_Supervisor\\supervisor.py"]
    ),
    # Day 10
    (
        "Build collaborative multi-agent network with shared state",
        ["12_Multi_Agent_Collaboration\\network.py"]
    ),
    # Day 11
    (
        "Deploy agents as production FastAPI endpoints",
        ["13_Agent_Serving_FastAPI\\api.py"]
    ),
    # Day 12
    (
        "Add agent evaluation framework with automated benchmarking",
        ["14_Agent_Evaluation\\eval.py"]
    ),
    # Day 13
    (
        "Build enterprise-grade agentic RAG with full orchestration",
        ["15_Enterprise_Agentic_RAG\\main.py"]
    ),
    # Day 14-15: README
    (
        "Add comprehensive project documentation and curriculum guide",
        ["README.md"]
    ),
]


def get_plan(repo_name=None):
    """Return the drip plan as a list of (message, files) tuples."""
    if repo_name == '15-Days-of-Advanced-Deep-Learning':
        return DRIP_PLAN_15_DAYS
    elif repo_name in ['-ml-algorithms-from-scratch', 'ml-algorithms-from-scratch']:
        return DRIP_PLAN_ML_PORTFOLIO
    elif repo_name == '15-Days-of-Agentic-AI':
        return DRIP_PLAN_AGENTIC_AI
    return None


if __name__ == "__main__":
    total_files = 0
    for day, (msg, files) in enumerate(DRIP_PLAN_15_DAYS, 1):
        print(f"\nDay {day}: {msg}")
        for f in files:
            print(f"  - {f}")
        total_files += len(files)
    print(f"\nTotal: {len(DRIP_PLAN_15_DAYS)} days, {total_files} files")
