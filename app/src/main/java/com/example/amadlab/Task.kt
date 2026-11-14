package com.example.amadlab

// The model: an immutable data class, changed only by creating copies
data class Task(
    val id: Long,
    val title: String,
    val done: Boolean = false
)
