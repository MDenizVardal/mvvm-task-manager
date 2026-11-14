package com.example.amadlab

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlin.math.roundToInt

// Task 3.4: everything the Statistics screen shows
data class StatisticsUiState(
    val total: Int = 0,
    val done: Int = 0
) {
    val remaining: Int get() = total - done
    val donePercent: Int get() = if (total == 0) 0 else (done * 100f / total).roundToInt()
}

class StatisticsViewModel(
    repository: TaskRepository = TaskRepository
) : ViewModel() {

    // derived from the same single source of truth as the other screens
    val uiState: StateFlow<StatisticsUiState> = repository.tasks
        .map { tasks -> StatisticsUiState(total = tasks.size, done = tasks.count { it.done }) }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5_000),
            initialValue = StatisticsUiState()
        )
}
